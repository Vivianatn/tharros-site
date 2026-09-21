"""Comptes joueurs : inscription, connexion (cookie httpOnly), profil, suppression (RGPD)."""
import random
from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlmodel import Session, select

from ..database import get_session
from ..models import Member, Subscriber
from ..schemas import MemberLoginIn, MemberOut, MemberRegisterIn, MemberUpdateIn, OkOut, PasswordChangeIn
from ..security import CurrentMember, OptionalMember, clear_member_cookie, hash_password, set_member_cookie, verify_password
from ..services.antispam import check_form, check_rate_limit, client_ip

router = APIRouter(prefix="/api/account", tags=["compte"])
SessionDep = Annotated[Session, Depends(get_session)]


@router.post("/register", response_model=MemberOut, status_code=201)
def register(data: MemberRegisterIn, request: Request, response: Response, session: SessionDep):
    ip = client_ip(request)
    if not check_form(data.website, data.elapsed, ip, "register"):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Inscription refusée")
    email = data.email.lower()
    if session.exec(select(Member).where(Member.email == email)).first():
        raise HTTPException(status.HTTP_409_CONFLICT, "Un compte existe déjà avec cette adresse")
    avatar = data.avatar or f"a{random.randint(1, 40):02d}"
    member = Member(email=email, password_hash=hash_password(data.password), display_name=data.display_name.strip(), avatar=avatar, newsletter=data.newsletter, last_login_at=datetime.now(timezone.utc))
    session.add(member)
    if data.newsletter and session.exec(select(Subscriber).where(Subscriber.email == email)).first() is None:
        session.add(Subscriber(email=email, ip=ip))
    session.commit()
    session.refresh(member)
    set_member_cookie(response, member)
    return member


@router.post("/login", response_model=MemberOut)
def login(data: MemberLoginIn, request: Request, response: Response, session: SessionDep):
    check_rate_limit("member-login:" + client_ip(request))
    member = session.exec(select(Member).where(Member.email == data.email.lower())).first()
    if member is None or not verify_password(data.password, member.password_hash):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "E-mail ou mot de passe incorrect")
    member.last_login_at = datetime.now(timezone.utc)
    session.add(member)
    session.commit()
    session.refresh(member)
    set_member_cookie(response, member)
    return member


@router.post("/logout", response_model=OkOut)
def logout(response: Response):
    clear_member_cookie(response)
    return OkOut(message="Déconnecté")


@router.get("/me", response_model=MemberOut | None)
def me(member: OptionalMember):
    return member


@router.put("/me", response_model=MemberOut)
def update_me(data: MemberUpdateIn, member: CurrentMember, session: SessionDep):
    member.display_name = data.display_name.strip()
    member.avatar = data.avatar
    member.newsletter = data.newsletter
    session.add(member)
    session.commit()
    session.refresh(member)
    return member


@router.post("/password", response_model=OkOut)
def change_password(data: PasswordChangeIn, member: CurrentMember, session: SessionDep):
    if not verify_password(data.current_password, member.password_hash):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Mot de passe actuel incorrect")
    member.password_hash = hash_password(data.new_password)
    session.add(member)
    session.commit()
    return OkOut(message="Mot de passe modifié")


@router.delete("/me", response_model=OkOut)
def delete_me(member: CurrentMember, response: Response, session: SessionDep):
    """Droit à l'effacement : supprime le compte et ses données."""
    session.delete(member)
    session.commit()
    clear_member_cookie(response)
    return OkOut(message="Compte supprimé")

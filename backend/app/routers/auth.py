from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlmodel import Session, select

from ..database import get_session
from ..models import User
from ..schemas import LoginIn, OkOut, PasswordChangeIn, TokenOut
from ..security import CurrentUser, create_access_token, hash_password, verify_password
from ..services.antispam import check_rate_limit, client_ip

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/login", response_model=TokenOut)
def login(data: LoginIn, request: Request, session: Annotated[Session, Depends(get_session)]):
    check_rate_limit("login:" + client_ip(request))
    user = session.exec(select(User).where(User.email == data.email.lower())).first()
    if user is None or not verify_password(data.password, user.password_hash):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Identifiants incorrects")
    return TokenOut(access_token=create_access_token(user), display_name=user.display_name)


@router.get("/me")
def me(user: CurrentUser):
    return {"id": user.id, "email": user.email, "display_name": user.display_name}


@router.post("/password", response_model=OkOut)
def change_password(data: PasswordChangeIn, user: CurrentUser, session: Annotated[Session, Depends(get_session)]):
    if not verify_password(data.current_password, user.password_hash):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Mot de passe actuel incorrect")
    user.password_hash = hash_password(data.new_password)
    session.add(user)
    session.commit()
    return OkOut(message="Mot de passe modifié")

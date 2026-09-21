"""Hachage des mots de passe (bcrypt) et jetons d'accès (JWT)."""
from datetime import datetime, timedelta, timezone
from typing import Annotated

import bcrypt
import jwt
from fastapi import Depends, HTTPException, Request, Response, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlmodel import Session, select

from .config import get_settings
from .database import get_session
from .models import Member, User

ALGORITHM = "HS256"
bearer = HTTPBearer(auto_error=False)


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, password_hash: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode(), password_hash.encode())
    except ValueError:
        return False


def create_access_token(user: User) -> str:
    settings = get_settings()
    expires = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_minutes)
    payload = {"sub": str(user.id), "email": user.email, "role": "admin", "exp": expires}
    return jwt.encode(payload, settings.secret_key, algorithm=ALGORITHM)


# ---------- Comptes joueurs : jeton dans un cookie httpOnly (les liens de téléchargement fonctionnent sans JavaScript)
def set_member_cookie(response: Response, member: Member) -> None:
    settings = get_settings()
    expires = datetime.now(timezone.utc) + timedelta(days=settings.member_token_days)
    token = jwt.encode({"sub": str(member.id), "role": "member", "exp": expires}, settings.secret_key, algorithm=ALGORITHM)
    response.set_cookie(
        settings.member_cookie, token, max_age=settings.member_token_days * 86400,
        httponly=True, samesite="lax", secure=settings.environment == "production", path="/",
    )


def clear_member_cookie(response: Response) -> None:
    response.delete_cookie(get_settings().member_cookie, path="/")


def get_optional_member(request: Request, session: Annotated[Session, Depends(get_session)]) -> Member | None:
    token = request.cookies.get(get_settings().member_cookie)
    if not token:
        return None
    try:
        payload = jwt.decode(token, get_settings().secret_key, algorithms=[ALGORITHM])
    except jwt.PyJWTError:
        return None
    if payload.get("role") != "member":
        return None
    return session.get(Member, int(payload["sub"]))


def get_current_member(member: Annotated[Member | None, Depends(get_optional_member)]) -> Member:
    if member is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Connexion requise")
    return member


OptionalMember = Annotated[Member | None, Depends(get_optional_member)]
CurrentMember = Annotated[Member, Depends(get_current_member)]


def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)],
    session: Annotated[Session, Depends(get_session)],
) -> User:
    unauthorized = HTTPException(status.HTTP_401_UNAUTHORIZED, "Authentification requise")
    if credentials is None:
        raise unauthorized
    try:
        payload = jwt.decode(credentials.credentials, get_settings().secret_key, algorithms=[ALGORITHM])
    except jwt.PyJWTError:
        raise unauthorized
    if payload.get("role") != "admin":
        raise unauthorized
    user = session.exec(select(User).where(User.id == int(payload["sub"]))).first()
    if user is None:
        raise unauthorized
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]

"""Téléchargement des builds de jeux (public, éventuellement réservé aux membres connectés)."""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlmodel import Session

from ..config import get_settings
from ..database import get_session
from ..models import Game, GameBuild
from ..security import OptionalMember

router = APIRouter(prefix="/api/downloads", tags=["téléchargements"])
BUILDS_DIR = "builds"


def build_path(filename: str):
    return get_settings().media_dir / BUILDS_DIR / filename


@router.get("/{build_id}")
def download(build_id: int, member: OptionalMember, session: Annotated[Session, Depends(get_session)]):
    build = session.get(GameBuild, build_id)
    game = session.get(Game, build.game_id) if build else None
    if build is None or game is None or not game.published:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Fichier introuvable")
    if game.download_requires_account and member is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Connectez-vous pour télécharger ce jeu")
    path = build_path(build.filename)
    if not path.is_file():
        raise HTTPException(status.HTTP_410_GONE, "Fichier indisponible")
    build.downloads += 1
    session.add(build)
    session.commit()
    return FileResponse(path, filename=build.original_name, media_type="application/octet-stream")

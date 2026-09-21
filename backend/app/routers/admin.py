"""Administration : CRUD complet sur le contenu. Toutes les routes exigent un jeton valide."""
import secrets
from datetime import datetime, timezone
from pathlib import Path
from typing import Annotated, Any

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from slugify import slugify
from sqlmodel import Session, select

from ..config import get_settings
from ..database import get_session
from ..models import FaqItem, Game, GameBuild, Media, Member, Message, Post, Setting, Subscriber
from ..schemas import (
    PLATFORMS, BuildOut, FaqIn, FaqOut, GameIn, GameOut, MediaOut, MediaUpdateIn, MemberAdminOut, MessageOut, OkOut,
    PostIn, PostOut, SettingOut, SubscriberOut,
)
from .downloads import BUILDS_DIR, build_path
from .public import game_out
from ..security import get_current_user
from ..services.images import ImageError, store_upload
from ..services.mail import mail_mode, send_mail

router = APIRouter(prefix="/api/admin", tags=["admin"], dependencies=[Depends(get_current_user)])
SessionDep = Annotated[Session, Depends(get_session)]


def _unique_slug(session: Session, model, wanted: str, exclude_id: int | None = None) -> str:
    base = slugify(wanted) or "element"
    slug, n = base, 2
    while True:
        existing = session.exec(select(model).where(model.slug == slug)).first()
        if existing is None or existing.id == exclude_id:
            return slug
        slug = f"{base}-{n}"
        n += 1


def _get_or_404(session: Session, model, item_id: int):
    item = session.get(model, item_id)
    if item is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Élément introuvable")
    return item


# ---------- Tableau de bord
@router.get("/dashboard")
def dashboard(session: SessionDep) -> dict[str, Any]:
    return {
        "posts": len(session.exec(select(Post)).all()),
        "posts_published": len(session.exec(select(Post).where(Post.published == True)).all()),  # noqa: E712
        "games": len(session.exec(select(Game)).all()),
        "faq": len(session.exec(select(FaqItem)).all()),
        "subscribers": len(session.exec(select(Subscriber)).all()),
        "messages_unread": len(session.exec(select(Message).where(Message.read == False)).all()),  # noqa: E712
        "media": len(session.exec(select(Media)).all()),
        "members": len(session.exec(select(Member)).all()),
    }


# ---------- Courrier
@router.get("/mail/status")
def mail_status():
    s = get_settings()
    return {"mode": mail_mode(), "to": s.mail_to, "from": s.mail_from, "smtp_host": s.smtp_host, "smtp_user": s.smtp_user}


@router.post("/mail/test", response_model=OkOut)
async def mail_test(user: Annotated[Any, Depends(get_current_user)]):
    """Envoie un e-mail de test à MAIL_TO pour vérifier la configuration."""
    try:
        await send_mail("[Tharros] E-mail de test", f"Ceci est un e-mail de test envoyé depuis l'administration par {user.email}. Si vous le lisez, la configuration fonctionne.", raise_errors=True)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status.HTTP_502_BAD_GATEWAY, f"Envoi impossible : {exc}")
    return OkOut(message=f"E-mail de test envoyé à {get_settings().mail_to}")


# ---------- Journal
@router.get("/posts", response_model=list[PostOut])
def list_posts(session: SessionDep):
    posts = session.exec(select(Post)).all()
    return sorted(posts, key=lambda p: p.published_at or p.created_at, reverse=True)


@router.post("/posts", response_model=PostOut, status_code=201)
def create_post(data: PostIn, session: SessionDep):
    post = Post(**data.model_dump(exclude={"slug"}))
    post.slug = _unique_slug(session, Post, data.slug or data.title)
    if post.published and post.published_at is None:
        post.published_at = datetime.now(timezone.utc)
    session.add(post)
    session.commit()
    session.refresh(post)
    return post


@router.put("/posts/{post_id}", response_model=PostOut)
def update_post(post_id: int, data: PostIn, session: SessionDep):
    post = _get_or_404(session, Post, post_id)
    for k, v in data.model_dump(exclude={"slug"}).items():
        setattr(post, k, v)
    if data.slug:
        post.slug = _unique_slug(session, Post, data.slug, exclude_id=post_id)
    if post.published and post.published_at is None:
        post.published_at = datetime.now(timezone.utc)
    post.updated_at = datetime.now(timezone.utc)
    session.add(post)
    session.commit()
    session.refresh(post)
    return post


@router.delete("/posts/{post_id}", response_model=OkOut)
def delete_post(post_id: int, session: SessionDep):
    session.delete(_get_or_404(session, Post, post_id))
    session.commit()
    return OkOut()


# ---------- Jeux
@router.get("/games", response_model=list[GameOut])
def list_games(session: SessionDep):
    return [game_out(g, session) for g in session.exec(select(Game).order_by(Game.sort_order)).all()]


@router.post("/games", response_model=GameOut, status_code=201)
def create_game(data: GameIn, session: SessionDep):
    game = Game(**data.model_dump(exclude={"slug"}))
    game.slug = _unique_slug(session, Game, data.slug or data.title)
    session.add(game)
    session.commit()
    session.refresh(game)
    return game_out(game, session)


@router.put("/games/{game_id}", response_model=GameOut)
def update_game(game_id: int, data: GameIn, session: SessionDep):
    game = _get_or_404(session, Game, game_id)
    for k, v in data.model_dump(exclude={"slug"}).items():
        setattr(game, k, v)
    if data.slug:
        game.slug = _unique_slug(session, Game, data.slug, exclude_id=game_id)
    game.updated_at = datetime.now(timezone.utc)
    session.add(game)
    session.commit()
    session.refresh(game)
    return game_out(game, session)


@router.delete("/games/{game_id}", response_model=OkOut)
def delete_game(game_id: int, session: SessionDep):
    game = _get_or_404(session, Game, game_id)
    for b in session.exec(select(GameBuild).where(GameBuild.game_id == game_id)).all():
        build_path(b.filename).unlink(missing_ok=True)
        session.delete(b)
    session.delete(game)
    session.commit()
    return OkOut()


# ---------- Builds téléchargeables
BUILD_EXTENSIONS = {".zip", ".7z", ".rar", ".exe", ".msi", ".dmg", ".pkg", ".appimage", ".deb", ".rpm", ".gz", ".tgz", ".xz", ".tar"}


@router.post("/games/{game_id}/builds", response_model=BuildOut, status_code=201)
async def upload_build(game_id: int, session: SessionDep, file: UploadFile = File(...), platform: str = Form(...), version: str = Form("")):
    """Téléverse un build en flux (fichiers volumineux) et remplace celui déjà présent pour la plateforme."""
    game = _get_or_404(session, Game, game_id)
    if platform not in PLATFORMS:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "Plateforme inconnue (windows, macos, linux)")
    original = Path(file.filename or "build").name
    if Path(original).suffix.lower() not in BUILD_EXTENSIONS:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "Format non pris en charge (zip, 7z, exe, msi, dmg, pkg, AppImage, deb, rpm, tar.gz)")
    limit = get_settings().max_build_mb * 1024 * 1024
    dest_dir = get_settings().media_dir / BUILDS_DIR
    dest_dir.mkdir(parents=True, exist_ok=True)
    filename = f"{game.slug}-{platform}-{secrets.token_hex(4)}{Path(original).suffix.lower()}"
    dest = dest_dir / filename
    size = 0
    with dest.open("wb") as out:
        while chunk := await file.read(1024 * 1024):
            size += len(chunk)
            if size > limit:
                out.close()
                dest.unlink(missing_ok=True)
                raise HTTPException(status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, f"Fichier trop lourd (max {get_settings().max_build_mb} Mo)")
            out.write(chunk)
    # un seul build par plateforme : on remplace l'ancien
    for old in session.exec(select(GameBuild).where(GameBuild.game_id == game_id, GameBuild.platform == platform)).all():
        build_path(old.filename).unlink(missing_ok=True)
        session.delete(old)
    build = GameBuild(game_id=game_id, platform=platform, version=version.strip()[:40], filename=filename, original_name=original, size_bytes=size)
    session.add(build)
    game.updated_at = datetime.now(timezone.utc)
    session.add(game)
    session.commit()
    session.refresh(build)
    return build


@router.delete("/games/{game_id}/builds/{build_id}", response_model=OkOut)
def delete_build(game_id: int, build_id: int, session: SessionDep):
    build = _get_or_404(session, GameBuild, build_id)
    if build.game_id != game_id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Élément introuvable")
    build_path(build.filename).unlink(missing_ok=True)
    session.delete(build)
    session.commit()
    return OkOut()


# ---------- Membres (comptes joueurs)
@router.get("/members", response_model=list[MemberAdminOut])
def list_members(session: SessionDep):
    return session.exec(select(Member).order_by(Member.created_at.desc())).all()


@router.delete("/members/{member_id}", response_model=OkOut)
def delete_member(member_id: int, session: SessionDep):
    session.delete(_get_or_404(session, Member, member_id))
    session.commit()
    return OkOut()


# ---------- FAQ
@router.get("/faq", response_model=list[FaqOut])
def list_faq(session: SessionDep):
    return session.exec(select(FaqItem).order_by(FaqItem.sort_order)).all()


@router.post("/faq", response_model=FaqOut, status_code=201)
def create_faq(data: FaqIn, session: SessionDep):
    item = FaqItem(**data.model_dump())
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@router.put("/faq/{item_id}", response_model=FaqOut)
def update_faq(item_id: int, data: FaqIn, session: SessionDep):
    item = _get_or_404(session, FaqItem, item_id)
    for k, v in data.model_dump().items():
        setattr(item, k, v)
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@router.delete("/faq/{item_id}", response_model=OkOut)
def delete_faq(item_id: int, session: SessionDep):
    session.delete(_get_or_404(session, FaqItem, item_id))
    session.commit()
    return OkOut()


# ---------- Réglages / blocs de contenu
@router.get("/settings", response_model=list[SettingOut])
def list_settings(session: SessionDep):
    return session.exec(select(Setting)).all()


@router.put("/settings/{key}", response_model=SettingOut)
def put_setting(key: str, value: dict[str, Any], session: SessionDep):
    setting = session.get(Setting, key) or Setting(key=key)
    setting.value = value
    setting.updated_at = datetime.now(timezone.utc)
    session.add(setting)
    session.commit()
    session.refresh(setting)
    return setting


# ---------- Médias
@router.get("/media", response_model=list[MediaOut])
def list_media(session: SessionDep):
    return session.exec(select(Media).order_by(Media.created_at.desc())).all()


@router.post("/media", response_model=MediaOut, status_code=201)
async def upload_media(session: SessionDep, file: UploadFile = File(...), alt: str = Form("")):
    content = await file.read()
    try:
        path, w, h = store_upload(content, file.content_type or "", file.filename or "image")
    except ImageError as exc:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, str(exc))
    media = Media(filename=path.name, url=f"/media/{path.name}", alt=alt, width=w, height=h, size_bytes=path.stat().st_size)
    session.add(media)
    session.commit()
    session.refresh(media)
    return media


@router.patch("/media/{media_id}", response_model=MediaOut)
def update_media(media_id: int, data: MediaUpdateIn, session: SessionDep):
    media = _get_or_404(session, Media, media_id)
    media.alt = data.alt
    session.add(media)
    session.commit()
    session.refresh(media)
    return media


@router.delete("/media/{media_id}", response_model=OkOut)
def delete_media(media_id: int, session: SessionDep):
    media = _get_or_404(session, Media, media_id)
    (get_settings().media_dir / media.filename).unlink(missing_ok=True)
    session.delete(media)
    session.commit()
    return OkOut()


# ---------- Messages et abonnés
@router.get("/messages", response_model=list[MessageOut])
def list_messages(session: SessionDep):
    return session.exec(select(Message).order_by(Message.created_at.desc())).all()


@router.patch("/messages/{message_id}/read", response_model=MessageOut)
def mark_read(message_id: int, session: SessionDep):
    msg = _get_or_404(session, Message, message_id)
    msg.read = True
    session.add(msg)
    session.commit()
    session.refresh(msg)
    return msg


@router.delete("/messages/{message_id}", response_model=OkOut)
def delete_message(message_id: int, session: SessionDep):
    session.delete(_get_or_404(session, Message, message_id))
    session.commit()
    return OkOut()


@router.get("/subscribers", response_model=list[SubscriberOut])
def list_subscribers(session: SessionDep):
    return session.exec(select(Subscriber).order_by(Subscriber.consented_at.desc())).all()


@router.delete("/subscribers/{sub_id}", response_model=OkOut)
def delete_subscriber(sub_id: int, session: SessionDep):
    session.delete(_get_or_404(session, Subscriber, sub_id))
    session.commit()
    return OkOut()

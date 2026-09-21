"""Lecture publique du contenu (aucune authentification) + formulaires + sitemap."""
from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlmodel import Session, select

from ..config import get_settings
from ..database import get_session
from ..models import FaqItem, Game, GameBuild, Message, Post, Setting, Subscriber
from ..schemas import BuildOut, ContactIn, FaqOut, GameOut, OkOut, PostOut, SubscribeIn
from ..services.antispam import check_form, client_ip
from ..services.mail import send_mail

router = APIRouter(prefix="/api", tags=["public"])
SessionDep = Annotated[Session, Depends(get_session)]


def game_out(game: Game, session: Session) -> GameOut:
    """Fiche de jeu avec ses builds téléchargeables (sans le nom de fichier interne)."""
    builds = session.exec(select(GameBuild).where(GameBuild.game_id == game.id).order_by(GameBuild.platform)).all()
    data = GameOut.model_validate(game, from_attributes=True)
    data.builds = [BuildOut.model_validate(b, from_attributes=True) for b in builds]
    return data


def _published_posts(session: Session):
    now = datetime.now(timezone.utc)
    posts = session.exec(select(Post).where(Post.published == True)).all()  # noqa: E712
    posts = [p for p in posts if p.published_at is None or p.published_at.replace(tzinfo=timezone.utc) <= now]
    return sorted(posts, key=lambda p: p.published_at or p.created_at, reverse=True)


@router.get("/content")
def site_content(session: SessionDep):
    """Tout ce dont le front public a besoin en une requête : réglages, jeux, derniers billets, FAQ."""
    settings = {s.key: s.value for s in session.exec(select(Setting)).all()}
    games = session.exec(select(Game).where(Game.published == True).order_by(Game.sort_order)).all()  # noqa: E712
    faq = session.exec(select(FaqItem).where(FaqItem.published == True).order_by(FaqItem.sort_order)).all()  # noqa: E712
    posts = _published_posts(session)[:3]
    return {
        "settings": settings,
        "games": [game_out(g, session) for g in games],
        "latest_posts": [PostOut.model_validate(p, from_attributes=True) for p in posts],
        "faq": [FaqOut.model_validate(f, from_attributes=True) for f in faq],
    }


@router.get("/posts", response_model=list[PostOut])
def list_posts(session: SessionDep):
    return _published_posts(session)


@router.get("/posts/{slug}", response_model=PostOut)
def get_post(slug: str, session: SessionDep):
    post = session.exec(select(Post).where(Post.slug == slug)).first()
    if post is None or post not in _published_posts(session):
        raise HTTPException(404, "Billet introuvable")
    return post


@router.get("/games/{slug}", response_model=GameOut)
def get_game(slug: str, session: SessionDep):
    game = session.exec(select(Game).where(Game.slug == slug, Game.published == True)).first()  # noqa: E712
    if game is None:
        raise HTTPException(404, "Jeu introuvable")
    return game_out(game, session)


@router.post("/subscribe", response_model=OkOut)
async def subscribe(data: SubscribeIn, request: Request, session: SessionDep):
    ip = client_ip(request)
    if not check_form(data.website, data.elapsed, ip, "subscribe"):
        return OkOut(message="Merci !")  # robot piégé : on fait semblant
    email = data.email.lower()
    if session.exec(select(Subscriber).where(Subscriber.email == email)).first() is None:
        session.add(Subscriber(email=email, ip=ip))
        session.commit()
        await send_mail("[Tharros] Nouvelle inscription à la liste d'attente", f"E-mail : {email}\nIP : {ip}")
    return OkOut(message="Bienvenue dans la légion. Vous recevrez les nouvelles de Muses en avant-première.")


@router.post("/contact", response_model=OkOut)
async def contact(data: ContactIn, request: Request, session: SessionDep):
    ip = client_ip(request)
    if not check_form(data.website, data.elapsed, ip, "contact"):
        return OkOut(message="Merci !")
    session.add(Message(name=data.name, email=data.email, subject=data.subject, body=data.message, ip=ip))
    session.commit()
    await send_mail(
        f"[Tharros] {data.subject} — {data.name}",
        f"Nom : {data.name}\nE-mail : {data.email}\n\n{data.message}\n\n— IP : {ip}",
        reply_to=data.email,
    )
    return OkOut(message="Merci, votre message a bien été envoyé. Réponse sous cinq jours ouvrés.")


@router.get("/sitemap.xml", include_in_schema=False)
def sitemap(session: SessionDep):
    base = get_settings().site_url.rstrip("/")
    today = datetime.now(timezone.utc).date().isoformat()
    static = ["/", "/jeux", "/journal", "/studio", "/presse", "/faq", "/contact", "/confidentialite", "/cgu", "/mentions-legales"]
    urls = [(p, today) for p in static]
    urls += [(f"/jeux/{g.slug}", g.updated_at.date().isoformat()) for g in session.exec(select(Game).where(Game.published == True)).all()]  # noqa: E712
    urls += [(f"/journal/{p.slug}", p.updated_at.date().isoformat()) for p in _published_posts(session)]
    body = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    body += "".join(f"  <url><loc>{base}{u}</loc><lastmod>{d}</lastmod></url>\n" for u, d in urls)
    body += "</urlset>\n"
    return Response(body, media_type="application/xml")

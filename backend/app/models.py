"""Tables de la base de données.

Le contenu éditorial du site est entièrement administrable :
- Post      : billets du journal de développement
- Game      : fiches de jeux (Muses…)
- FaqItem   : questions fréquentes
- Setting   : blocs de contenu libres (accueil, studio, presse, pages légales…) stockés en JSON
- Media     : fichiers téléversés (images optimisées en WebP)
- Subscriber / Message : données reçues via les formulaires publics
"""
from datetime import datetime, timezone
from typing import Any, Optional

from sqlalchemy import JSON, Column
from sqlmodel import Field, SQLModel


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    password_hash: str
    display_name: str = "Admin"
    created_at: datetime = Field(default_factory=utcnow)


class Post(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    slug: str = Field(index=True, unique=True)
    title: str
    excerpt: str = ""
    body_md: str = ""
    tag: str = "Devlog"
    cover_url: Optional[str] = None
    embed_url: Optional[str] = None  # animation interactive du devlog (page HTML autonome)
    published: bool = False
    published_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=utcnow)
    updated_at: datetime = Field(default_factory=utcnow)


class Game(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    slug: str = Field(index=True, unique=True)
    title: str
    status: str = "En développement"
    tagline: str = ""
    pitch_md: str = ""
    cover_url: Optional[str] = None
    banner_url: Optional[str] = None
    specs: list[dict[str, str]] = Field(default_factory=list, sa_column=Column(JSON))
    pillars: list[dict[str, str]] = Field(default_factory=list, sa_column=Column(JSON))
    progress: list[dict[str, str]] = Field(default_factory=list, sa_column=Column(JSON))
    featured: bool = False
    published: bool = True
    sort_order: int = 0
    download_requires_account: bool = False
    updated_at: datetime = Field(default_factory=utcnow)


class GameBuild(SQLModel, table=True):
    """Fichier téléchargeable d'un jeu pour une plateforme (windows / macos / linux)."""

    id: Optional[int] = Field(default=None, primary_key=True)
    game_id: int = Field(foreign_key="game.id", index=True)
    platform: str = Field(index=True)
    version: str = ""
    filename: str
    original_name: str
    size_bytes: int = 0
    downloads: int = 0
    created_at: datetime = Field(default_factory=utcnow)


class Member(SQLModel, table=True):
    """Compte joueur (inscription publique), distinct des administrateurs."""

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    password_hash: str
    display_name: str
    avatar: str = "001"  # identifiant d'un des 100 avatars prédéfinis (frontend/public/avatars)
    newsletter: bool = False
    created_at: datetime = Field(default_factory=utcnow)
    last_login_at: Optional[datetime] = None


class FaqItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    question: str
    answer_md: str
    sort_order: int = 0
    published: bool = True


class Setting(SQLModel, table=True):
    """Bloc de contenu identifié par une clé (ex. "home", "studio", "legal.cgu")."""

    key: str = Field(primary_key=True)
    value: dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))
    updated_at: datetime = Field(default_factory=utcnow)


class Media(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    filename: str
    url: str
    alt: str = ""
    width: Optional[int] = None
    height: Optional[int] = None
    size_bytes: int = 0
    created_at: datetime = Field(default_factory=utcnow)


class Subscriber(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    ip: str = ""
    consented_at: datetime = Field(default_factory=utcnow)


class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    subject: str
    body: str
    ip: str = ""
    read: bool = False
    created_at: datetime = Field(default_factory=utcnow)

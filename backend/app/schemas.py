"""Schémas Pydantic : ce que l'API accepte et renvoie."""
from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, EmailStr, Field, field_validator


# ---------- Auth
class LoginIn(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=200)


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    display_name: str


class PasswordChangeIn(BaseModel):
    current_password: str
    new_password: str = Field(min_length=10, max_length=200)


# ---------- Journal
class PostIn(BaseModel):
    title: str = Field(min_length=1, max_length=160)
    slug: Optional[str] = Field(default=None, max_length=160)
    excerpt: str = Field(default="", max_length=400)
    body_md: str = ""
    tag: str = Field(default="Devlog", max_length=40)
    cover_url: Optional[str] = None
    embed_url: Optional[str] = None
    published: bool = False
    published_at: Optional[datetime] = None


class PostOut(PostIn):
    id: int
    slug: str
    created_at: datetime
    updated_at: datetime


# ---------- Jeux
class KeyValue(BaseModel):
    k: str = Field(max_length=60)
    v: str = Field(max_length=300)


class Pillar(BaseModel):
    num: str = Field(default="", max_length=8)
    title: str = Field(max_length=80)
    text: str = Field(max_length=600)


PLATFORMS = ("windows", "macos", "linux")


class BuildOut(BaseModel):
    id: int
    platform: str
    version: str
    original_name: str
    size_bytes: int
    downloads: int = 0
    created_at: datetime


class GameIn(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    slug: Optional[str] = Field(default=None, max_length=120)
    status: str = Field(default="En développement", max_length=60)
    tagline: str = Field(default="", max_length=300)
    pitch_md: str = ""
    cover_url: Optional[str] = None
    banner_url: Optional[str] = None
    specs: list[KeyValue] = []
    pillars: list[Pillar] = []
    progress: list[KeyValue] = []
    featured: bool = False
    published: bool = True
    sort_order: int = 0
    download_requires_account: bool = False


class GameOut(GameIn):
    id: int
    slug: str
    updated_at: datetime
    builds: list[BuildOut] = []


# ---------- FAQ
class FaqIn(BaseModel):
    question: str = Field(min_length=1, max_length=200)
    answer_md: str = Field(min_length=1)
    sort_order: int = 0
    published: bool = True


class FaqOut(FaqIn):
    id: int


# ---------- Réglages / contenu libre
class SettingOut(BaseModel):
    key: str
    value: dict[str, Any]
    updated_at: datetime


# ---------- Médias
class MediaOut(BaseModel):
    id: int
    filename: str
    url: str
    alt: str
    width: Optional[int]
    height: Optional[int]
    size_bytes: int
    created_at: datetime


class MediaUpdateIn(BaseModel):
    alt: str = Field(max_length=300)


class EmbedOut(BaseModel):
    url: str
    size_bytes: int


# ---------- Formulaires publics
class AntiSpamMixin(BaseModel):
    website: str = ""  # pot de miel : doit rester vide
    elapsed: float = Field(default=0, description="millisecondes passées sur le formulaire")
    consent: bool

    @field_validator("consent")
    @classmethod
    def must_consent(cls, v: bool) -> bool:
        if not v:
            raise ValueError("Le consentement est requis")
        return v


class SubscribeIn(AntiSpamMixin):
    email: EmailStr


class ContactIn(AntiSpamMixin):
    name: str = Field(min_length=2, max_length=80)
    email: EmailStr
    subject: str = Field(min_length=1, max_length=120)
    message: str = Field(min_length=20, max_length=4000)


class MessageOut(BaseModel):
    id: int
    name: str
    email: str
    subject: str
    body: str
    read: bool
    created_at: datetime


class SubscriberOut(BaseModel):
    id: int
    email: str
    consented_at: datetime


# ---------- Comptes joueurs
AVATAR_RE = r"^(0[0-9][1-9]|0[1-9][0-9]|100)$"  # 001 … 100


class MemberRegisterIn(AntiSpamMixin):
    email: EmailStr
    password: str = Field(min_length=10, max_length=200)
    display_name: str = Field(min_length=2, max_length=60)
    avatar: Optional[str] = Field(default=None, pattern=AVATAR_RE)
    newsletter: bool = False


class MemberLoginIn(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=200)


class MemberOut(BaseModel):
    id: int
    email: str
    display_name: str
    avatar: str
    newsletter: bool
    created_at: datetime


class MemberUpdateIn(BaseModel):
    display_name: str = Field(min_length=2, max_length=60)
    avatar: str = Field(pattern=AVATAR_RE)
    newsletter: bool = False


class MemberAdminOut(MemberOut):
    last_login_at: Optional[datetime]


class OkOut(BaseModel):
    ok: bool = True
    message: str = ""

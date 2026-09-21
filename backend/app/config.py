"""Configuration de l'application, lue depuis l'environnement / le fichier .env."""
from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_DIR = Path(__file__).resolve().parent.parent
PROJECT_DIR = BACKEND_DIR.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=PROJECT_DIR / ".env", env_file_encoding="utf-8", extra="ignore")

    # --- Application
    app_name: str = "Tharros"
    site_url: str = "http://localhost:8000"
    environment: str = Field(default="development", pattern="^(development|production|test)$")
    database_url: str = f"sqlite:///{BACKEND_DIR / 'tharros.db'}"
    media_dir: Path = BACKEND_DIR / "media"
    frontend_dist: Path = PROJECT_DIR / "frontend" / "dist"
    cors_origins: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]

    # --- Sécurité
    secret_key: str = "change-me-in-production-please"
    access_token_minutes: int = 60 * 12
    admin_email: str = "admin@tharros-studio.fr"
    admin_password: str = "tharros-admin"  # utilisé uniquement à la création du premier compte

    # --- Courrier : destinataire des notifications + service d'envoi (SMTP Gmail ou Resend)
    mail_to: str = "tharrs.studio@gmail.com"
    mail_from: str = "Tharros <tharrs.studio@gmail.com>"
    smtp_host: str = ""          # ex. smtp.gmail.com
    smtp_port: int = 587
    smtp_user: str = ""          # ex. tharrs.studio@gmail.com
    smtp_password: str = ""      # mot de passe d'application Google (16 caractères)
    resend_api_key: str = ""     # alternative à SMTP

    # --- Anti-spam
    min_form_seconds: float = 3.0
    rate_limit_max: int = 10
    rate_limit_window_seconds: int = 600

    # --- Médias
    max_upload_mb: int = 10
    image_max_width: int = 2000
    max_build_mb: int = 4000  # taille maximale d'un build de jeu
    member_cookie: str = "tharros_member"
    member_token_days: int = 30


@lru_cache
def get_settings() -> Settings:
    return Settings()

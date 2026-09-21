"""Optimisation des images téléversées : redimensionnement et conversion en WebP."""
import io
import secrets
from pathlib import Path

from PIL import Image, UnidentifiedImageError

from ..config import get_settings

ALLOWED_RASTER = {"image/png", "image/jpeg", "image/webp", "image/gif"}
ALLOWED_VECTOR = {"image/svg+xml"}


class ImageError(ValueError):
    pass


def store_upload(content: bytes, content_type: str, original_name: str) -> tuple[Path, int | None, int | None]:
    """Enregistre le fichier dans media_dir ; renvoie (chemin, largeur, hauteur)."""
    settings = get_settings()
    settings.media_dir.mkdir(parents=True, exist_ok=True)
    if len(content) > settings.max_upload_mb * 1024 * 1024:
        raise ImageError(f"Fichier trop lourd (max {settings.max_upload_mb} Mo)")
    token = secrets.token_hex(6)

    if content_type in ALLOWED_VECTOR:
        if b"<script" in content.lower():
            raise ImageError("SVG refusé : contient un script")
        path = settings.media_dir / f"{token}.svg"
        path.write_bytes(content)
        return path, None, None

    if content_type not in ALLOWED_RASTER:
        raise ImageError("Format non pris en charge (PNG, JPEG, WebP, GIF ou SVG)")
    try:
        img = Image.open(io.BytesIO(content))
        img.load()
    except UnidentifiedImageError as exc:
        raise ImageError("Image illisible") from exc

    if img.mode not in ("RGB", "RGBA"):
        img = img.convert("RGBA" if "A" in img.getbands() else "RGB")
    if img.width > settings.image_max_width:
        ratio = settings.image_max_width / img.width
        img = img.resize((settings.image_max_width, round(img.height * ratio)), Image.LANCZOS)

    path = settings.media_dir / f"{token}.webp"
    img.save(path, "WEBP", quality=82, method=6)
    return path, img.width, img.height

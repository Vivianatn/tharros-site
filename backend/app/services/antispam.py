"""Protection des formulaires publics : pot de miel, délai minimal, limitation de débit par IP."""
import time
from collections import defaultdict, deque

from fastapi import HTTPException, Request, status

from ..config import get_settings

_hits: dict[str, deque[float]] = defaultdict(deque)


def client_ip(request: Request) -> str:
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


def check_rate_limit(ip: str) -> None:
    settings = get_settings()
    now = time.monotonic()
    window = _hits[ip]
    while window and now - window[0] > settings.rate_limit_window_seconds:
        window.popleft()
    if len(window) >= settings.rate_limit_max:
        raise HTTPException(status.HTTP_429_TOO_MANY_REQUESTS, "Trop de tentatives, réessayez plus tard")
    window.append(now)


def check_form(website: str, elapsed_ms: float, ip: str, bucket: str = "form") -> bool:
    """Renvoie False si l'envoi ressemble à un robot (pot de miel rempli) : on répondra OK sans rien faire."""
    if website:
        return False
    if elapsed_ms < get_settings().min_form_seconds * 1000:
        raise HTTPException(status.HTTP_429_TOO_MANY_REQUESTS, "Formulaire envoyé trop vite")
    check_rate_limit(f"{bucket}:{ip}")
    return True

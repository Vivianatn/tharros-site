"""Point d'entrée FastAPI.

- /api/...        API JSON (publique + admin)
- /media/...      fichiers téléversés
- /*              front Vue compilé (frontend/dist) avec repli SPA — en développement, Vite sert le front sur :5173
"""
import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlmodel import Session

from .config import get_settings
from .database import engine, init_db
from .routers import admin, auth, downloads, members, public
from .seed import seed

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    with Session(engine) as session:
        seed(session)
    settings.media_dir.mkdir(parents=True, exist_ok=True)
    yield


app = FastAPI(title="Tharros API", version="1.0.0", lifespan=lifespan, docs_url="/api/docs", redoc_url=None, openapi_url="/api/openapi.json")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def security_headers(request: Request, call_next):
    response = await call_next(request)
    if request.url.path.startswith("/assets/"):
        response.headers.setdefault("Cache-Control", "public, max-age=31536000, immutable")  # noms de fichiers hachés
    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("X-Frame-Options", "DENY")
    response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
    response.headers.setdefault("Permissions-Policy", "camera=(), microphone=(), geolocation=()")
    if settings.environment == "production":
        response.headers.setdefault("Strict-Transport-Security", "max-age=63072000; includeSubDomains; preload")
    return response


app.include_router(auth.router)
app.include_router(public.router)
app.include_router(admin.router)
app.include_router(members.router)
app.include_router(downloads.router)
app.mount("/media", StaticFiles(directory=settings.media_dir, check_dir=False), name="media")

# ---------- Front compilé (production)
dist: Path = settings.frontend_dist
if (dist / "index.html").exists():
    app.mount("/assets", StaticFiles(directory=dist / "assets"), name="assets")

    NO_CACHE = {"Cache-Control": "no-cache"}  # index.html : toujours revalidé, sinon un ancien HTML demande des assets disparus

    @app.api_route("/{full_path:path}", methods=["GET", "HEAD"], include_in_schema=False)
    async def spa(full_path: str):
        candidate = dist / full_path
        if full_path and candidate.is_file():
            return FileResponse(candidate, headers=NO_CACHE if candidate.suffix in (".html", ".webmanifest", ".txt") else None)
        # Route inconnue : le routeur Vue affiche sa page 404 ; on renvoie quand même le bon code HTTP
        known_prefixes = ("", "jeux", "journal", "studio", "presse", "faq", "contact", "confidentialite", "cgu", "mentions-legales", "admin", "compte")
        first = full_path.split("/", 1)[0]
        status = 200 if first in known_prefixes else 404
        return FileResponse(dist / "index.html", status_code=status, headers=NO_CACHE)
else:

    @app.get("/", include_in_schema=False)
    async def no_front():
        return JSONResponse({"message": "API Tharros en ligne. Le front n'est pas compilé : lancez `npm run build` dans frontend/ ou utilisez dev.bat."})

"""Moteur SQLModel et session par requête."""
from collections.abc import Generator

from sqlmodel import Session, SQLModel, create_engine

from .config import get_settings

settings = get_settings()

connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
engine = create_engine(settings.database_url, connect_args=connect_args)


def init_db() -> None:
    from sqlalchemy import inspect, text

    from . import models  # noqa: F401  (enregistre les tables)

    SQLModel.metadata.create_all(engine)
    # Migration légère : ajoute les colonnes apparues après la création de la base (SQLite ne le fait pas seul)
    inspector = inspect(engine)
    with engine.begin() as conn:
        for table in SQLModel.metadata.sorted_tables:
            existing = {c["name"] for c in inspector.get_columns(table.name)}
            for column in table.columns:
                if column.name not in existing:
                    ddl = f'ALTER TABLE "{table.name}" ADD COLUMN "{column.name}" {column.type.compile(engine.dialect)}'
                    default = column.default.arg if column.default is not None and not callable(column.default.arg) else None
                    if default is not None:
                        ddl += f" DEFAULT {int(default) if isinstance(default, bool) else repr(default)}"
                    conn.execute(text(ddl))
    _migrate_avatar_ids()


def _migrate_avatar_ids() -> None:
    """Les avatars sont passés de 40 (« a07 ») à 100 (« 007 ») : on convertit les comptes existants."""
    from sqlalchemy import inspect, text

    with engine.begin() as conn:
        if "member" not in inspect(engine).get_table_names():
            return
        rows = conn.execute(text("SELECT id, avatar FROM member WHERE avatar LIKE 'a%'")).fetchall()
        for member_id, avatar in rows:
            number = avatar[1:]
            new = f"{int(number):03d}" if number.isdigit() and 1 <= int(number) <= 100 else "001"
            conn.execute(text("UPDATE member SET avatar = :a WHERE id = :i"), {"a": new, "i": member_id})


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

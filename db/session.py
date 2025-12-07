from typing import Tuple, Optional
from urllib.parse import urlparse
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session
from psycopg2.extensions import connection as PsycopgConnection, cursor as PsycopgCursor


def _close_connection(conn: PsycopgConnection, cur: PsycopgCursor) -> None:
    try:
        cur.close()
    finally:
        conn.close()


def _init_connection(admin_url: str) -> Tuple[PsycopgConnection, PsycopgCursor]:
    try:
        import psycopg2
        conn = psycopg2.connect(admin_url)
        conn.autocommit = True
        cur = conn.cursor()
        return conn, cur
    except Exception as exc:
        raise RuntimeError("Failed to initialize admin connection.") from exc


def _fetch_first_row(cur: PsycopgCursor, dbname: str) -> Optional[tuple]:
    try:
        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s;", (dbname,))
        return cur.fetchone()
    except Exception as exc:
        raise RuntimeError("Failed to execute existence check query.") from exc


def _create_if_not_exist(cur: PsycopgCursor, dbname: str, exists: Optional[tuple]) -> None:
    if not exists:
        try:
            cur.execute(f'CREATE DATABASE "{dbname}"')
        except Exception as exc:
            raise RuntimeError(f"Failed to create database '{dbname}'.") from exc


class DBSession:
    """Database session manager with optional Alembic support."""

    def __init__(self, url: str, use_alembic: bool = False) -> None:
        self.url = url
        self._use_alembic = use_alembic
        if not self._use_alembic:
            self._ensure_database_exists()
        try:
            self.engine = create_engine(url, echo=False, future=True)
            self.SessionFactory = sessionmaker(bind=self.engine, expire_on_commit=False, class_=Session)
        except Exception as exc:
            raise RuntimeError("Failed to initialize SQLAlchemy engine.") from exc

    def get_session(self) -> Session:
        return self.SessionFactory()

    def get_engine(self) -> Engine:
        return self.engine

    def _ensure_database_exists(self) -> None:
        admin_url, dbname = self._init_admin_url()
        conn: Optional[PsycopgConnection] = None
        cur: Optional[PsycopgCursor] = None
        try:
            conn, cur = _init_connection(admin_url)
            exists = _fetch_first_row(cur, dbname)
            _create_if_not_exist(cur, dbname, exists)
        except Exception as exc:
            raise RuntimeError(f"Failed to ensure database '{dbname}' exists.") from exc
        finally:
            if conn and cur:
                _close_connection(conn, cur)

    def _init_admin_url(self) -> Tuple[str, str]:
        try:
            parsed = urlparse(self.url)
            dbname = parsed.path.lstrip("/")
            admin_url = self.url.replace(f"/{dbname}", "/postgres")
            return admin_url, dbname
        except Exception as exc:
            raise RuntimeError("Failed to parse database URL.") from exc

from typing import Tuple, Optional
from urllib.parse import urlparse
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session
from psycopg2.extensions import connection as PsycopgConnection, cursor as PsycopgCursor


def _close_connection(conn: PsycopgConnection, cur: PsycopgCursor) -> None:
    """Close psycopg2 cursor and connection safely.

    Args:
        conn (PsycopgConnection): Database connection object.
        cur (PsycopgCursor): Cursor to be closed.
    """
    try:
        cur.close()
    finally:
        conn.close()


def _init_connection(admin_url: str) -> Tuple[PsycopgConnection, PsycopgCursor]:
    """Initialize admin-level PostgreSQL connection.

    Args:
        admin_url (str): Connection string for admin database.

    Returns:
        Tuple[PsycopgConnection, PsycopgCursor]: Active connection and cursor.

    Raises:
        RuntimeError: When connection initialization fails.
    """
    try:
        import psycopg2
        conn = psycopg2.connect(admin_url)
        conn.autocommit = True
        cur = conn.cursor()
        return conn, cur
    except Exception as exc:
        raise RuntimeError("Failed to initialize admin connection.") from exc


def _fetch_first_row(cur: PsycopgCursor, dbname: str) -> Optional[tuple]:
    """Check if database exists by querying PostgreSQL metadata.

    Args:
        cur (PsycopgCursor): Active cursor.
        dbname (str): Name of the database to check.

    Returns:
        Optional[tuple]: Result row if exists, otherwise None.

    Raises:
        RuntimeError: When query execution fails.
    """
    try:
        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s;", (dbname,))
        return cur.fetchone()
    except Exception as exc:
        raise RuntimeError("Failed to execute existence check query.") from exc


def _create_if_not_exist(cur: PsycopgCursor, dbname: str, exists: Optional[tuple]) -> None:
    """Create database when not already present.

    Args:
        cur (PsycopgCursor): Active cursor.
        dbname (str): Database name.
        exists (Optional[tuple]): Query result indicating existence.

    Raises:
        RuntimeError: When database creation fails.
    """
    if not exists:
        try:
            cur.execute(f'CREATE DATABASE "{dbname}"')
        except Exception as exc:
            raise RuntimeError(f"Failed to create database '{dbname}'.") from exc


class DBSession:
    """Database session manager using SQLAlchemy."""

    def __init__(self, url: str, use_alembic: bool = False) -> None:
        """Initialize session manager.

        Args:
            url (str): SQLAlchemy connection URL.
            use_alembic (bool): Whether migrations are controlled externally.

        Raises:
            RuntimeError: When engine creation fails.
        """
        self.url = url
        self._use_alembic = use_alembic
        if not self._use_alembic:
            self._ensure_database_exists()
        try:
            self.engine = create_engine(url, echo=False, future=True)
            self.SessionFactory = sessionmaker(
                bind=self.engine, expire_on_commit=False, class_=Session
            )
        except Exception as exc:
            raise RuntimeError("Failed to initialize SQLAlchemy engine.") from exc

    def get_session(self) -> Session:
        """Return new SQLAlchemy session instance.

        Returns:
            Session: Newly created database session.
        """
        return self.SessionFactory()

    def get_engine(self) -> Engine:
        """Return SQLAlchemy engine instance.

        Returns:
            Engine: Active database engine.
        """
        return self.engine

    def _ensure_database_exists(self) -> None:
        """Ensure the target database is created.

        Raises:
            RuntimeError: When existence check or creation fails.
        """
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
        """Convert user database URL to admin-accessible URL.

        Returns:
            Tuple[str, str]: Admin URL and database name.

        Raises:
            RuntimeError: When URL parsing fails.
        """
        try:
            parsed = urlparse(self.url)
            dbname = parsed.path.lstrip("/")
            admin_url = self.url.replace(f"/{dbname}", "/postgres")
            return admin_url, dbname
        except Exception as exc:
            raise RuntimeError("Failed to parse database URL.") from exc

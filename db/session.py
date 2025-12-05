from typing import Tuple, Optional
from urllib.parse import urlparse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from psycopg2.extensions import connection as PsycopgConnection, cursor as PsycopgCursor


def _close_connection(conn: PsycopgConnection, cur: PsycopgCursor) -> None:
    """Close psycopg2 cursor and connection.

    Args:
        conn (PsycopgConnection): Active connection.
        cur (PsycopgCursor): Active cursor.

    Returns:
        None: No return value.

    Raises:
        None
    """
    try:
        cur.close()
    finally:
        conn.close()


def _init_connection(admin_url: str) -> Tuple[PsycopgConnection, PsycopgCursor]:
    """Initialize a psycopg2 connection and cursor for admin operations.

    Args:
        admin_url (str): Connection URL for a Postgres admin database.

    Returns:
        Tuple[PsycopgConnection, PsycopgCursor]: Connection and cursor.

    Raises:
        RuntimeError: If connection creation fails.
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
    """Check whether a database exists by fetching a row from pg_database.

    Args:
        cur (PsycopgCursor): Active cursor.
        dbname (str): Database name to check.

    Returns:
        Optional[tuple]: First matching row or None.

    Raises:
        RuntimeError: If query execution fails.
    """
    try:
        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s;", (dbname,))
        return cur.fetchone()
    except Exception as exc:
        raise RuntimeError("Failed to execute existence check query.") from exc


def _create_if_not_exist(cur: PsycopgCursor, dbname: str, exists: Optional[tuple]) -> None:
    """Create database if it does not exist.

    Args:
        cur (PsycopgCursor): Active cursor.
        dbname (str): Database name to create.
        exists (Optional[tuple]): Result from existence check.

    Returns:
        None: No return value.

    Raises:
        RuntimeError: If creation fails.
    """
    if not exists:
        try:
            cur.execute(f'CREATE DATABASE "{dbname}"')
        except Exception as exc:
            raise RuntimeError(f"Failed to create database '{dbname}'.") from exc


class DBSession:
    """Database session manager with automatic database creation.

    Attributes:
        url (str): SQLAlchemy database URL.
        engine: SQLAlchemy engine instance.
        SessionFactory: Factory for SQLAlchemy sessions.
    """

    def __init__(self, url: str) -> None:
        """Initialize DBSession and ensure database exists.

        Args:
            url (str): SQLAlchemy database URL in format postgresql://user:pass@host:port/dbname

        Returns:
            None: No return value.

        Raises:
            RuntimeError: If database creation or engine initialization fails.
        """
        self.url = url
        self._ensure_database_exists()
        try:
            self.engine = create_engine(url, echo=False, future=True)
            self.SessionFactory = sessionmaker(bind=self.engine, expire_on_commit=False, class_=Session)
        except Exception as exc:
            raise RuntimeError("Failed to initialize SQLAlchemy engine.") from exc

    def get_session(self) -> Session:
        """Return a new SQLAlchemy session.

        Args:
            None

        Returns:
            Session: New SQLAlchemy session.

        Raises:
            None
        """
        return self.SessionFactory()

    def _ensure_database_exists(self) -> None:
        """Ensure the target database exists, creating it if necessary.

        Args:
            None

        Returns:
            None: No return value.

        Raises:
            RuntimeError: If admin operations fail.
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
        """Create admin URL and extract database name from configured URL.

        Args:
            None

        Returns:
            Tuple[str, str]: Admin URL and database name.

        Raises:
            RuntimeError: If URL parsing fails.
        """
        try:
            parsed = urlparse(self.url)
            dbname = parsed.path.lstrip("/")
            admin_url = self.url.replace(f"/{dbname}", "/postgres")
            return admin_url, dbname
        except Exception as exc:
            raise RuntimeError("Failed to parse database URL.") from exc

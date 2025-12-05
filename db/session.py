from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session


def _close_connection(conn, cur):
    cur.close()
    conn.close()


def _init_connection(admin_url):
    import psycopg2
    conn = psycopg2.connect(admin_url)
    conn.autocommit = True
    cur = conn.cursor()
    return conn, cur


def _fetch_first_row(cur, dbname):
    cur.execute("SELECT 1 FROM pg_database WHERE datname = %s;", (dbname,))
    exists = cur.fetchone()
    return exists


def _create_if_not_exist(cur, dbname, exists):
    if not exists:
        cur.execute(f'CREATE DATABASE "{dbname}"')


class DBSession:
    """Database session manager with auto-create for missing PostgreSQL databases."""

    def __init__(self, url: str):
        """
        Args:
            url (str): SQLAlchemy database URL in format postgresql://user:pass@host:port/dbname
        """
        self.url = url
        self._ensure_database_exists()
        self.engine = create_engine(url, echo=False, future=True)
        self.SessionFactory = sessionmaker(bind=self.engine, expire_on_commit=False, class_=Session)

    def get_session(self) -> Session:
        """Return a new session."""
        return self.SessionFactory()

    def _ensure_database_exists(self) -> None:
        """Check if target database exists, create it if missing."""
        admin_url, dbname = self._init_admin_url()
        try:
            conn, cur = _init_connection(admin_url)
            exists = _fetch_first_row(cur, dbname)
            _create_if_not_exist(cur, dbname, exists)
            _close_connection(conn, cur)
        except Exception as e:
            raise RuntimeError(f"Failed to ensure database '{dbname}' exists.") from e

    def _init_admin_url(self):
        from urllib.parse import urlparse
        parsed = urlparse(self.url)
        dbname = parsed.path.lstrip("/")
        admin_url = self.url.replace(f"/{dbname}", "/postgres")
        return admin_url, dbname
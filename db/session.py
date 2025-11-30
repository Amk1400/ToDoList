import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from urllib.parse import urlparse

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
        from urllib.parse import urlparse
        import psycopg2

        parsed = urlparse(self.url)
        dbname = parsed.path.lstrip("/")
        admin_url = self.url.replace(f"/{dbname}", "/postgres")  # connect to default db

        try:
            conn = psycopg2.connect(admin_url)
            conn.autocommit = True  # بسیار مهم برای CREATE DATABASE
            cur = conn.cursor()
            cur.execute("SELECT 1 FROM pg_database WHERE datname = %s;", (dbname,))
            exists = cur.fetchone()
            if not exists:
                cur.execute(f'CREATE DATABASE "{dbname}"')
            cur.close()
            conn.close()
        except Exception as e:
            raise RuntimeError(f"Failed to ensure database '{dbname}' exists.") from e


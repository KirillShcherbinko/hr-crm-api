from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.config.settings import settings

sync_db_url = settings.DATABASE_URL.replace(
    "postgresql+asyncpg", "postgresql+psycopg2")

# Создаём синхронный движок
sync_engine = create_engine(
    sync_db_url,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    echo=False
)

# Фабрика сессий
sync_session_factory = sessionmaker(
    bind=sync_engine,
    autocommit=False,
    autoflush=False)


@contextmanager
def get_sync_session():
    """
    Синхронный контекстный менеджер для сессий БД в Celery.
    Использование: with get_sync_session() as session: ...
    """
    session = sync_session_factory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

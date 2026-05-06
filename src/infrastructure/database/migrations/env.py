from src.infrastructure.database.models import Base
from src.config.settings import settings
import os
import sys
from pathlib import Path
import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine

# 1. Добавляем корень проекта в sys.path
# env.py -> migrations -> database -> infrastructure -> src -> root
PROJECT_ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(PROJECT_ROOT))

# 2. ИМПОРТИРУЕМ ЭКЗЕМПЛЯР НАСТРОЕК (именно `import settings`, а не модуль)

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    # Для offline-режима убираем +asyncpg, т.к. Alembic генерирует чистый SQL
    url = settings.DATABASE_URL.replace("postgresql+asyncpg", "postgresql")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    # Асинхронный движок берёт URL из settings
    engine = create_async_engine(
        settings.DATABASE_URL,
        poolclass=pool.NullPool)
    async with engine.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await engine.dispose()


def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

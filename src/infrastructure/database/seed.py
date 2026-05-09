from src.infrastructure.database.models.enums import UserRole
from src.infrastructure.database.models.pipeline import PipelineTemplate, PipelineTemplateStage
from src.infrastructure.database.models.user import User
from src.config.settings import settings
import asyncio
import sys
from pathlib import Path
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession


PROJECT_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PROJECT_ROOT))


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def seed_database() -> None:
    if not settings.DATABASE_URL:
        raise ValueError("DATABASE_URL не указан в переменных окружения")

    # Создаём изолированный движок и сессию для инициализации
    engine = create_async_engine(settings.DATABASE_URL, echo=False)
    session_factory = async_sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False)

    async with session_factory() as session:
        try:
            print("🔍 Проверка существующих данных...")

            # 1. Администратор
            admin_email = "admin@hr-crm.local"
            admin_stmt = select(User).where(User.email == admin_email)
            if not (await session.execute(admin_stmt)).scalar_one_or_none():
                session.add(User(
                    email=admin_email,
                    hashed_password=pwd_context.hash("AdminSecure123!"[:72]),
                    full_name="System Administrator",
                    role=UserRole.admin,
                    is_active=True
                ))
                print("✅ Администратор создан.")

            # 2. Рекрутер по умолчанию
            recruiter_email = "recruiter@hr-crm.local"
            rec_stmt = select(User).where(User.email == recruiter_email)
            if not (await session.execute(rec_stmt)).scalar_one_or_none():
                session.add(User(
                    email=recruiter_email,
                    hashed_password=pwd_context.hash("RecruiterSecure123!"),
                    full_name="Default Recruiter",
                    role=UserRole.recruiter,
                    is_active=True
                ))
                print("✅ Рекрутер создан.")

            # 3. Шаблон воронки "Стандартный найм"
            tpl_stmt = select(PipelineTemplate).where(
                PipelineTemplate.name == "Стандартный найм")
            if not (await session.execute(tpl_stmt)).scalar_one_or_none():
                creator_stmt = select(User).where(
                    User.email == recruiter_email)
                creator = (await session.execute(creator_stmt)).scalar_one_or_none()
                if not creator:
                    creator_stmt = select(User).where(
                        User.role == UserRole.admin)
                    creator = (await session.execute(creator_stmt)).scalar_one()

                template = PipelineTemplate(
                    name="Стандартный найм", created_by=creator.id)
                # Благодаря cascade="all, delete-orphan" этапы сохранятся
                # автоматически
                template.stages = [
                    PipelineTemplateStage(name="Новый отклик", order_index=0),
                    PipelineTemplateStage(
                        name="Телефонный скрининг", order_index=1),
                    PipelineTemplateStage(
                        name="Техническое интервью", order_index=2),
                    PipelineTemplateStage(
                        name="Финальное интервью", order_index=3),
                    PipelineTemplateStage(
                        name="Оффер", order_index=4, is_final=True),
                    PipelineTemplateStage(
                        name="Отказ", order_index=5, is_final=True),
                ]
                session.add(template)
                print("✅ Шаблон воронки создан.")

            await session.commit()
            print("🌱 Инициализация базы данных завершена успешно.")

        except Exception as e:
            await session.rollback()
            print(f"❌ Ошибка инициализации: {e}")
            raise
        finally:
            await engine.dispose()

if __name__ == "__main__":
    print("🚀 Запуск скрипта инициализации данных...")
    asyncio.run(seed_database())

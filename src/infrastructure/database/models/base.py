from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Базовый класс для всех ORM-моделей.
    Использует декларативный стиль, принятый в SQLAlchemy 2.0.
    От этого класса наследуются все сущности в папке models.
    """
    pass

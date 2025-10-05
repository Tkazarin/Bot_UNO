from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, declared_attr, sessionmaker

from config import get_database_url

DATABASE_URL = get_database_url()

engine = create_engine(DATABASE_URL)

session_maker = sessionmaker(bind=engine)

# Базовый класс для моделей
class Base(DeclarativeBase):
    abstract = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

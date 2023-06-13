from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession,
                                    create_async_engine)
from sqlalchemy.orm import sessionmaker

from settings import settings

DATABASE_URL: str = (
    'postgresql+asyncpg://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}'.format(
        USER=settings.USER,
        PASSWORD=settings.PASSWORD,
        HOST=settings.HOST,
        PORT=settings.PORT,
        DB_NAME=settings.DB_NAME
    )
)

engine: AsyncEngine = create_async_engine(DATABASE_URL)


def create_session() -> AsyncSession:
    """
    Функция для обертки sqlalchemy.sessionmaker'а
    Создает и возвращает объект async session
    """
    return sessionmaker(
        bind=engine, class_=AsyncSession,
        expire_on_commit=False, autoflush=False
    )()

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.library_catalog.settings import DatabaseSettings

db_settings = DatabaseSettings()
engine = create_async_engine(db_settings.url, echo=True, future=True)
session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncGenerator[AsyncSession]:
    async with session_maker() as session:
        yield session

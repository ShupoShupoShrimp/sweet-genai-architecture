from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from sugar.core.settings import get_settings

setting = get_settings()

engine = create_async_engine(
    setting.database_url.get_secret_value(),
    pool_pre_ping=True,
    expire_on_commit=False,
)

SessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def get_db() -> AsyncGenerator[AsyncSession]:
    async with SessionLocal() as session:
        yield session

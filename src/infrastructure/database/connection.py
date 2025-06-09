from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine

import src.settings

settings = src.settings.get_settings(db=True)

engine = create_async_engine(f"{settings.get_db_uri}")


async def get_db() -> AsyncSession:
    async_session = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()

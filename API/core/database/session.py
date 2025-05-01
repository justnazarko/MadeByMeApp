"""Database session and utils"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine

from API.core.config import config
from API.core.database.jsonencoder import custom_serializer

engine = create_async_engine(
    config.db.url,
    json_serializer=custom_serializer,
    pool_size=25,  # Number of connections to keep in the pool
    max_overflow=15,  # Additional connections allowed beyond pool_size
    pool_timeout=30,  # Timeout for getting a connection from the pool
)
Session = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def get_session():
    """
    Get the database session.
    This can be used for dependency injection.

    :return: The database session.
    """
    session = Session()
    try:
        yield session
    except Exception as exc:
        await session.rollback()
        raise exc
    finally:
        await session.close()

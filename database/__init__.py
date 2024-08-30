from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlmodel import SQLModel

from config import config

db_url = (
    "postgresql+asyncpg://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_async_engine(
    db_url.format(
        DB_USERNAME=config.database.username,
        DB_PASSWORD=config.database.password,
        DB_HOST=config.database.host,
        DB_PORT=config.database.port,
        DB_NAME=config.database.db,
    ),
    echo=False,
)

sessionmaker = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def init_db():
    async with engine.begin() as conn:
        # await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session():
    async with sessionmaker() as session:
        yield session


async def teardown():
    await engine.dispose()

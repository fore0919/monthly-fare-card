from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.core.config import settings

engine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    # connect_args=ENGINE_CONNECTION_ARGS,
    pool_pre_ping=True,
    **settings.SQLALCHEMY_ENGINE_OPTIONS
)

async_session = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base
from pydantic_settings import BaseSettings, SettingsConfigDict



class Setting(BaseSettings):
    database_url: str
    model_config = SettingsConfigDict(env_file='.env')


settings = Setting()
engine = create_async_engine(settings.database_url)


AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()

async def get_db():
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
     await db.close()
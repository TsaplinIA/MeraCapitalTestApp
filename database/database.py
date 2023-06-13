from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, AsyncAttrs
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.inspection import inspect

from config import DATABASE_URL


class Base(AsyncAttrs, DeclarativeBase):
    pass


def default_repr(x: "Base") -> str:
    pk_name = inspect(x.__class__).primary_key[0].name
    pk_value = getattr(x, pk_name, "?")
    return f"({x.__class__.__name__} #{pk_value})"


Base.__repr__ = default_repr

engine = create_async_engine(DATABASE_URL, echo=False)
async_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import registry
from sqlalchemy.inspection import inspect

from config import DATABASE_URL

mapper_registry = registry()
Base = mapper_registry.generate_base()


def default_repr(x: "Base") -> str:
    pk_name = inspect(x.__class__).primary_key[0].name
    pk_value = getattr(x, pk_name, "?")
    return f"({x.__class__.__name__} #{pk_value})"


Base.__repr__ = default_repr

engine = create_async_engine(DATABASE_URL, echo=False)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Integer, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select
from sqlalchemy.engine import Result
import uuid

from database.database import Base


class Pricestamp(Base):
    __tablename__ = "pricestamps"
    pricestamp_idx = Column(UUID, primary_key=True, default=uuid.uuid4)
    ticker = Column(String(8), nullable=False)
    price = Column(Integer, nullable=False)
    timestamp = Column(Integer, nullable=False)

    @staticmethod
    async def create_pricestamp(ticker: str, price: int, timestamp: int, session: AsyncSession):
        new_pricestamp = Pricestamp(ticker=ticker, price=price, timestamp=timestamp)
        session.add(new_pricestamp)
        try:
            await session.commit()
            return new_pricestamp
        except:
            await session.rollback()
            raise

    @staticmethod
    async def get_pricestamps(session: AsyncSession, min_timestamp: int = None, max_timestamp: int = None):
        query: Select = select(Pricestamp)
        query: Select = query.filter(Pricestamp.timestamp >= min_timestamp) if min_timestamp is not None else query
        query: Select = query.filter(Pricestamp.timestamp <= max_timestamp) if max_timestamp is not None else query
        query: Select = query.order_by(Pricestamp.timestamp)
        query_result: Result = await session.execute(query)
        return query_result.scalars().all()

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Integer, select, ForeignKey
from sqlalchemy.orm import relationship, selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.associationproxy import association_proxy, AssociationProxy
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import Select, desc, text
from sqlalchemy.engine import Result

from database.database import Base


class Pricestamp(Base):
    __tablename__ = "pricestamps"

    pricestamp_idx = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    currency_idx = Column(UUID, ForeignKey('currencies.currency_idx'), nullable=False)
    price = Column(Integer, nullable=False)
    timestamp = Column(Integer, nullable=False)

    currency = relationship('Currency', cascade='save-update, merge, delete')
    ticker: AssociationProxy[str] = association_proxy('currency', 'ticker')

    @staticmethod
    async def create_pricestamp(currency_idx: str, price: int, timestamp: int, session: AsyncSession):
        new_pricestamp = Pricestamp(currency_idx=currency_idx, price=price, timestamp=timestamp)
        session.add(new_pricestamp)
        try:
            await session.commit()
            print(f"Pricestamp {str(new_pricestamp.pricestamp_idx)} has been saved")
            return new_pricestamp
        except SQLAlchemyError:
            await session.rollback()
            raise

    @staticmethod
    async def get_pricestamps(session: AsyncSession, ticker: str, min_timestamp: int = None, max_timestamp: int = None):
        query: Select = select(Pricestamp)
        query: Select = query.filter(Pricestamp.ticker == ticker)
        query: Select = query.filter(Pricestamp.timestamp >= min_timestamp) if min_timestamp is not None else query
        query: Select = query.filter(Pricestamp.timestamp <= max_timestamp) if max_timestamp is not None else query
        query: Select = query.order_by(Pricestamp.timestamp)
        query: Select = query.options(selectinload(Pricestamp.currency))
        query_result: Result = await session.execute(query)
        return query_result.scalars().all()

    @staticmethod
    async def get_last_pricestamp(session: AsyncSession, ticker: str):
        query: Select = select(Pricestamp)
        query: Select = query.filter(Pricestamp.ticker == ticker)
        query: Select = query.order_by(desc(Pricestamp.timestamp))
        query: Select = query.limit(1)
        query: Select = query.options(selectinload(Pricestamp.currency))
        query_result: Result = await session.execute(query)
        return query_result.scalars().first()

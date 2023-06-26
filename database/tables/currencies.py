from uuid import UUID

from sqlalchemy.dialects.postgresql import UUID as POSTGRES_UUID
from sqlalchemy import Column, String, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import Select, text
from sqlalchemy.engine import Result
from fastapi import Depends

from database.database import Base, get_session
from config import DERIBIT_PUBLIC_API_URL


class Currency(Base):
    __tablename__ = "currencies"

    currency_idx = Column(POSTGRES_UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    ticker = Column(String(8), nullable=False, unique=True)
    index_price_name = Column(String(32), nullable=False, unique=True)

    def create_index_url(self) -> str:
        return f"{DERIBIT_PUBLIC_API_URL}/get_index_price?index_name={self.index_price_name}"

    @staticmethod
    async def get_all_currencies(session: AsyncSession = Depends(get_session)):
        query: Select = select(Currency)
        query_result: Result = await session.execute(query)
        return query_result.scalars().all()

    @staticmethod
    async def get_currency_by_idx(currency_idx: UUID, session: AsyncSession = Depends(get_session)):
        query: Select = select(Currency)
        query: Select = query.filter(Currency.currency_idx == currency_idx)
        query_result: Result = await session.execute(query)
        return query_result.scalars().first()

    @staticmethod
    async def create_currency(
            ticker: str,
            index_price_name: str,
            session: AsyncSession = Depends(get_session)
    ):
        new_currency = Currency(ticker=ticker, index_price_name=index_price_name)
        session.add(new_currency)
        try:
            await session.commit()
            return new_currency
        except SQLAlchemyError:
            await session.rollback()
            raise

    @staticmethod
    async def update_currency_by_idx(
            idx: UUID,
            new_ticker: str = None,
            new_index_price_name: str = None,
            session: AsyncSession = Depends(get_session)
    ):
        currency: Currency = await Currency.get_currency_by_idx(idx)
        currency.ticker = currency.ticker if new_ticker is None else new_ticker
        currency.index_price_name = currency.index_price_name if new_index_price_name is None else new_index_price_name
        try:
            await session.commit()
            return currency
        except SQLAlchemyError:
            await session.rollback()
            raise
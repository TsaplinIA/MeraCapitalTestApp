from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Integer, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select, desc
from sqlalchemy.engine import Result
import uuid

from database.database import Base
from config import DERIBIT_PUBLIC_API_URL


class Currency(Base):
    __tablename__ = "currencies"
    currency_idx = Column(UUID, primary_key=True, default=uuid.uuid4)
    ticker = Column(String(8), nullable=False)
    index_price_name = Column(String(32), nullable=False)

    def create_index_url(self) -> str:
        return f"{DERIBIT_PUBLIC_API_URL}/get_index_price?index_name={self.index_price_name}"

    @staticmethod
    async def get_all_currencies(session: AsyncSession):
        query: Select = select(Currency)
        query_result: Result = await session.execute(query)
        return query_result.scalars().all()

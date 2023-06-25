from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.models.currencies import CurrencyModel
from database import get_session, Currency

currencies_router = APIRouter()


@currencies_router.get(
    '/currency',
    summary="Get list of currencies",
    description="Get list of currencies from database",
    response_model=list[CurrencyModel],
)
async def get_currency_by_id_view(currencies: list[Currency] = Depends(Currency.get_all_currencies)):
    return currencies


@currencies_router.get('/currency/{currency_idx}')
async def get_currency_by_id_view(currency_idx: UUID):
    pass

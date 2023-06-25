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
async def get_currencies_view(currencies: list[Currency] = Depends(Currency.get_all_currencies)):
    return currencies


@currencies_router.get(
    '/currency/{currency_idx}',
    summary="Get currency",
    description="Get currency by idx(uuid)",
    response_model=CurrencyModel,
)
async def get_currency_by_id_view(currency_idx: UUID, currency: Currency = Depends(Currency.get_currency_by_idx)):
    if currency is None:
        raise HTTPException(detail=f"Currency with idx {currency_idx} not found", status_code=404)
    return currency


@currencies_router.post(
    '/currency',
    summary="Create currency",
    description="Create currency. Specify index_price_name and ticker",
    response_model=CurrencyModel,
)
async def create_currency_view(currency: Currency = Depends(Currency.create_currency)):
    return currency

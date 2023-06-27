from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.models.currencies import CurrencyModel, CurrencyCreateModel, CurrencyUpdateModel
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
async def get_currency_by_id_view(currency: Currency = Depends(Currency.get_currency_by_idx)):
    if currency is None:
        raise HTTPException(detail=f"Currency with this idx not found", status_code=404)
    return currency


@currencies_router.post(
    '/currency',
    summary="Create currency",
    description="Create currency. Specify index_price_name and ticker",
    response_model=CurrencyModel,
)
async def create_currency_view(
        data: CurrencyCreateModel,
        session: AsyncSession = Depends(get_session),
):
    currency = await Currency.create_currency(data.ticker, data.index_price_name, session)
    return currency


@currencies_router.patch(
    '/currency/{currency_idx}',
    summary="Update currency",
    description="Update currency. Specify index_price_name and ticker",
    response_model=CurrencyModel,
)
async def create_currency_view(
        currency_idx: UUID,
        data: CurrencyUpdateModel,
        session: AsyncSession = Depends(get_session),
):
    currency = await Currency.update_currency_by_idx(currency_idx, data.ticker, data.index_price_name, session)
    return currency


@currencies_router.delete(
    '/currency/{currency_idx}',
    summary="Delete currency",
    description="Delete currency by id",
    response_model=str,
)
async def create_currency_view(
        currency_idx: UUID,
        session: AsyncSession = Depends(get_session),
):
    is_deleted = await Currency.delete_currency(currency_idx, session)
    if not is_deleted:
        raise HTTPException(detail="Currency not found", status_code=404)
    return f"currency {currency_idx} has been deleted"

from typing import Literal

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.models import PricestampModel, GetPriceRequestModel
from database import get_session, Pricestamp

router = APIRouter()


@router.get(
    "/price_list",
    summary="Get list of pricestamps",
    description="Get list of pricestamps, use ticker and filter by date",
    response_model=list[PricestampModel],
)
async def get_price_list_view(data: GetPriceRequestModel = Depends(), session: AsyncSession = Depends(get_session)):
    result = await Pricestamp.get_pricestamps(
        session=session,
        ticker=data.ticker,
        min_timestamp=data.min_timestamp,
        max_timestamp=data.max_timestamp,
    )
    return result


@router.get(
    "/last_price",
    summary="Get last price",
    description="Get last price by tiker",
    response_model=PricestampModel,
)
async def get_last_price_view(ticker: Literal['BTC', 'ETH'], session: AsyncSession = Depends(get_session)):
    pricestamp = await Pricestamp.get_last_pricestamp(session=session, ticker=ticker)
    if pricestamp is None:
        raise HTTPException(detail=f"Pricestamp for {ticker} not found", status_code=404)
    return pricestamp


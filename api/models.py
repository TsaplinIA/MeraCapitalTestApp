from typing import Literal
from uuid import UUID
from pydantic.main import BaseModel, Field


class GetPriceRequestModel(BaseModel):
    ticker: Literal['BTC', 'ETH']
    min_timestamp: int = Field(None, example=0)
    max_timestamp: int = Field(None, example=1786657933)


class PricestampModel(BaseModel):
    pricestamp_idx: UUID = Field(..., example="ac3831fe-09e2-11ee-be56-0242ac120002")
    ticker: str = Field(..., example="BTC")
    price: int = Field(..., example=50000)
    timestamp: int = Field(..., example=1686657933)

    class Config:
        orm_mode = True

from uuid import UUID

from pydantic.fields import Field
from pydantic.main import BaseModel


class CurrencyModel(BaseModel):
    currency_idx: UUID = Field(..., example="ac3831fe-09e2-11ee-be56-0242ac120002")
    index_price_name: str = Field(..., example="btc_usd")
    ticker: str = Field(..., example="BTC")

    class Config:
        orm_mode = True

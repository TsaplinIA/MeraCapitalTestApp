from uuid import UUID

from pydantic.class_validators import root_validator
from pydantic.fields import Field
from pydantic.main import BaseModel


class CurrencyModel(BaseModel):
    currency_idx: UUID = Field(..., example="ac3831fe-09e2-11ee-be56-0242ac120002")
    index_price_name: str = Field(..., example="btc_usd")
    ticker: str = Field(..., example="BTC")

    class Config:
        orm_mode = True


class CurrencyCreateModel(BaseModel):
    index_price_name: str = Field(..., example="btc_usd")
    ticker: str = Field(..., example="BTC")


class CurrencyUpdateModel(BaseModel):
    index_price_name: str | None = Field(None, example="btc_usd")
    ticker: str | None = Field(None, example="BTC")

    @root_validator
    def check_not_empty_body(cls, values):
        if values['index_price_name'] is None and values['ticker'] is None:
            raise ValueError('need index_price_name or ticker')
        return values

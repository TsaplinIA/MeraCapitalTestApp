from uuid import UUID

from fastapi import HTTPException


class CurrencyNotFound(HTTPException):
    """Exception raised for case with wrong currency_idx."""

    def __init__(self, currency_idx: UUID):
        message = f"Currency with id {currency_idx} not found"
        super().__init__(detail=message, status_code=404)

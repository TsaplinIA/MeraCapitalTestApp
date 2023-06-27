from fastapi import HTTPException


class DuplicateKeyError(HTTPException):
    """Exception raised for duplicate key errors in SQLAlchemy."""

    def __init__(self, table_name, column_name, value):
        self.table_name = table_name
        self.column_name = column_name
        self.value = value
        message = f"Duplicate key error in table '{table_name}'. " \
                  f"Column '{column_name}' with value '{value}' already exists."
        super().__init__(detail=message, status_code=400)

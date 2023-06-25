from fastapi import FastAPI
import uvicorn

from api.endpoints.currencies import currencies_router
from api.endpoints.pricestamps import pricestamps_router

app = FastAPI(title="Mera Capital Test app")
app.include_router(pricestamps_router, tags=['pricestamps'])
app.include_router(currencies_router, tags=['currencies'])


def cli():
    uvicorn.run("api:app", port=5050, host="0.0.0.0", reload=True)


if __name__ == "__main__":
    cli()

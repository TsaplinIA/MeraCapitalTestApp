from fastapi import FastAPI
import uvicorn

from api.endpoints import router

app = FastAPI(title="Mera Capital Test app")
app.include_router(router)


def cli():
    uvicorn.run("api:app", port=5050, host="0.0.0.0", reload=True)


if __name__ == "__main__":
    cli()

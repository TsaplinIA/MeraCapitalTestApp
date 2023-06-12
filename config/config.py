import os

from starlette.config import Config

# Get path to .env file
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
env_location: list = __location__.split("/")
env_location[-1] = ".env"
env_location: str = "/".join(env_location)

config = Config(env_location)

__DB_USER = config("MC_DB_USER", cast=str, default="postgres")
__DB_PASSWORD = config("MC_DB_PASSWORD", cast=str, default="postgres")
__DB_HOST = config("MC_DB_HOST", cast=str, default="0.0.0.0")
__DB_NAME = config("MC_DB_NAME", cast=str, default="postgres")
__DB_PORT = config("MC_DB_PORT", cast=int, default=5432)

DATABASE_URL = f"postgresql+asyncpg://{__DB_USER}:{__DB_PASSWORD}@{__DB_HOST}:{__DB_PORT}/{__DB_NAME}"

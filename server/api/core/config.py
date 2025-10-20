import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings


def load_env():
    load_dotenv("../../.env")

    load_dotenv(".env.local", override=True)

load_env()

class Settings(BaseSettings):
    PROJECT_NAME: str = os.getenv("PROJECT_NAME")
    VERSION_API: str = os.getenv("VERSION_API")
    SECRET_KEY: str = os.getenv("SECRET_KEY")

    DB_URL: str = os.getenv("SQLALCHEMY_DATABASE_URL")

    ALGORITHM: str = os.getenv("ALGORITHM")

    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

    class Config:
        env_file = '.env.local'

settings = Settings()

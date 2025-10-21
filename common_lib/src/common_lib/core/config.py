import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings


def load_env():
    load_dotenv("../../../../.env")

load_env()

class GlobalSettings(BaseSettings):
    PROJECT_NAME: str = os.getenv("PROJECT_NAME")
    SECRET_KEY: str = os.getenv("SECRET_KEY")

    DB_URL: str = os.getenv("DB_URL")
    DB_NAME: str = os.getenv("DB_NAME")
    DB_USER: str = os.getenv("DB_USER")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")
    DB_HOST: str = os.getenv("DB_HOST")
    DB_PORT: str = os.getenv("DB_PORT")

    ALGORITHM: str = os.getenv("ALGORITHM")
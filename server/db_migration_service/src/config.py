import os

from common_lib.core.config import GlobalSettings


class DatabaseConfig(GlobalSettings):
    project_name: str = os.getenv('PROJECT_NAME')
    host: str = os.getenv('POSTGRES_ADDRESS')
    port: int = os.getenv('POSTGRES_PORT')
    name: str = os.getenv('POSTGRES_DB')
    user: str = os.getenv('POSTGRES_USER')
    password: str = os.getenv('POSTGRES_PASSWORD')
    url: str = os.getenv('SQLALCHEMY_DATABASE_URL')

config = DatabaseConfig()
import os
from dataclasses import dataclass

from common_lib.core.config import GlobalSettings
from common_lib.utils.custom_logger import CustomLogger


class DatabaseConfig(GlobalSettings):
    DB_SCHEMAS: str = 'public'

@dataclass
class FlywayConfig:
    migrations_location: str = os.getenv('MIGRATIONS_LOCATION', '/app/migrations')
    baseline_version: str = os.getenv('BASELINE_VERSION', '1')
    clean_on_validation_error: bool = os.getenv('CLEAN_ON_VALIDATION_ERROR', 'false').lower() == 'true'

class Config:
    db = DatabaseConfig()
    flyway = FlywayConfig()

custom_logger = CustomLogger(service_name='db_migration_service')
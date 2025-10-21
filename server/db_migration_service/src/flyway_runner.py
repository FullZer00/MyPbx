import subprocess
import os
from typing import List, Optional, Dict
from src.config import Config
from common_lib.utils import CustomLogger


class FlywayRunner:
    def __init__(self, config: Config):
        self.config = config
        self.logger = CustomLogger("db_migration_service")

    def _build_flyway_command(self, command: str, additional_args: List[str] = None) -> List[str]:
        """Собирает команду Flyway с базовыми параметрами"""
        cmd = [
            'flyway',
            f'-url=jdbc:postgresql://{self.config.db.DB_HOST}:{self.config.db.DB_PORT}/{self.config.db.DB_NAME}',
            f'-user={self.config.db.DB_USER}',
            f'-password={self.config.db.DB_PASSWORD}',
            f'-schemas={self.config.db.DB_SCHEMAS}',
            f'-locations=filesystem:{self.config.flyway.migrations_location}',
            f'-baselineVersion={self.config.flyway.baseline_version}',
        ]

        if self.config.flyway.clean_on_validation_error:
            cmd.append('-cleanOnValidationError=true')

        cmd.append(command)

        if additional_args:
            cmd.extend(additional_args)

        return cmd

    def _run_flyway_command(self, command: List[str]) -> bool:
        """Выполняет команду Flyway и обрабатывает результат"""
        self.logger.info(f"Executing: {' '.join(command)}")

        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=True
            )
            self.logger.info("Command executed successfully")
            self.logger.debug(f"Output: {result.stdout}")
            return True

        except subprocess.CalledProcessError as e:
            self.logger.error(f"Flyway command failed: {e}")
            self.logger.error(f"Error output: {e.stderr}")
            return False

    def migrate(self) -> bool:
        """Применяет все pending миграции"""
        self.logger.info("Starting database migration...")
        cmd = self._build_flyway_command('migrate')
        return self._run_flyway_command(cmd)

    def info(self) -> bool:
        """Показывает информацию о состоянии миграций"""
        self.logger.info("Getting migration info...")
        cmd = self._build_flyway_command('info')
        return self._run_flyway_command(cmd)

    def validate(self) -> bool:
        """Валидирует миграции"""
        self.logger.info("Validating migrations...")
        cmd = self._build_flyway_command('validate')
        return self._run_flyway_command(cmd)

    def clean(self) -> bool:
        """Очищает базу данных (осторожно!)"""
        self.logger.warning("Cleaning database - THIS WILL DELETE ALL DATA!")
        cmd = self._build_flyway_command('clean')
        return self._run_flyway_command(cmd)

    def baseline(self) -> bool:
        """Создает baseline для существующей БД"""
        self.logger.info("Creating database baseline...")
        cmd = self._build_flyway_command('baseline')
        return self._run_flyway_command(cmd)

    def repair(self) -> bool:
        """Чинит таблицу миграций"""
        self.logger.info("Repairing migration table...")
        cmd = self._build_flyway_command('repair')
        return self._run_flyway_command(cmd)

    def check_connection(self) -> bool:
        """Проверяет подключение к БД"""
        self.logger.info("Testing database connection...")
        self.logger.info(f"Host: {self.config.db.DB_HOST}\nPort: {self.config.db.DB_PORT}")
        try:
            import psycopg2
            conn = psycopg2.connect(
                host=self.config.db.DB_HOST,
                port=self.config.db.DB_PORT,
                database=self.config.db.DB_NAME,
                user=self.config.db.DB_USER,
                password=self.config.db.DB_PASSWORD
            )
            conn.close()
            self.logger.info("Database connection successful")
            return True
        except Exception as e:
            self.logger.error(f"Database connection failed: {e}")
            return False
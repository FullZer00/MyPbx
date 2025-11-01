import psycopg2
from common_lib.exceptions import DBException
from common_lib.utils.custom_logger import CustomLogger
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from src.config import Config
from src.flyway_runner import FlywayRunner


class InitRunner:
    def __init__(self, config: Config, init_file: str):
        self.config = config
        self.logger = CustomLogger(__name__)
        self.init_file = init_file

    def init(self) -> bool:
        flyway_runner = FlywayRunner(self.config)

        if not flyway_runner.check_connection():
            raise DBException(message='Cannot connect to DB server')

        try:
            if self._create_database():
                self.run_sql_file(self.init_file)
                return True
        except DBException as e:
            self.logger.error(message=f'Ошибка инициализации базы данных из файла {self.init_file}')
            return False


    def _create_database(self) -> bool:
        try:
            conn = psycopg2.connect(
                host=self.config.db.DB_HOST,
                port=self.config.db.DB_PORT,
                database='postgres',
                user=self.config.db.DB_USER,
                password=self.config.db.DB_PASSWORD
            )
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = conn.cursor()

            # Проверяем существует ли БД
            cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (self.config.db.DB_NAME,))
            exists = cursor.fetchone()

            if not exists:
                cursor.execute(f'CREATE DATABASE "{self.config.db.DB_NAME}"')
                self.logger.info(f"Database {self.config.db.DB_NAME} created")
            else:
                self.logger.info(f"Database {self.config.db.DB_NAME} already exists")

            cursor.close()
            conn.close()
            return True

        except Exception as e:
            self.logger.error(f"Failed to create database: {e}")
            return False

    def run_sql_file(self, file_path):
        try:
            with psycopg2.connect(
                    dbname=self.config.db.DB_NAME,
                    user=self.config.db.DB_USER,
                    password=self.config.db.DB_PASSWORD,
                    host=self.config.db.DB_HOST,
                    port=self.config.db.DB_PORT
            ) as conn:
                with conn.cursor() as cursor:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        sql = file.read()

                        cursor.execute(sql)

                        if cursor.description:
                            rows = cursor.fetchall()
                            for row in rows:
                                print(row)

                        conn.commit()
                        self.logger.info(message=f'Sql-файл {file_path} успешно выполнен')

        except DBException as e:
            self.logger.error(message=e.message)
            if conn:
                conn.rollback()
            raise e


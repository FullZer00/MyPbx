import sys
import argparse
from src.config import Config, custom_logger
from src.flyway_runner import FlywayRunner
<<<<<<< HEAD
from common_lib.utils import CustomLogger
=======
from src.init import InitRunner
>>>>>>> init_db


def main():
    parser = argparse.ArgumentParser(description='Database Migration Tool')
    parser.add_argument('command', choices=['migrate', 'info', 'validate', 'clean', 'baseline', 'repair', 'check', 'init'],
                        help='Flyway command to execute')
    parser.add_argument('--config', '-c', help='Path to config file')

    args = parser.parse_args()

    # Инициализация конфигурации
    config = Config()
    runner = FlywayRunner(config)
    init_runner = InitRunner(config, init_file="./src/init.sql")

    # Проверка подключения к БД перед выполнением команд
    if not runner.check_connection():
        custom_logger.structured_logger(message="ERROR: Cannot connect to database", level="ERROR")
        sys.exit(1)

    # Выполнение команды
    commands = {
        'migrate': runner.migrate,
        'info': runner.info,
        'validate': runner.validate,
        'clean': runner.clean,
        'baseline': runner.baseline,
        'repair': runner.repair,
        'check': runner.check_connection,
        'init': init_runner.init
    }

    success = commands[args.command]()
    if success:
        custom_logger.structured_logger(message=f'Команда {commands[args.command].__name__} успешно выполнена', level="INFO")
        sys.exit(0)
    else:
        custom_logger.structured_logger(message=f'Команда {commands[args.command].__name__} не выполнена', level="FATAL")
        sys.exit(1)


if __name__ == '__main__':
    main()
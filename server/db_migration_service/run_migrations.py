import sys
import argparse
from src.config import Config
from src.flyway_runner import FlywayRunner
from src.init import InitRunner


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
        runner.logger.error(message="ERROR: Cannot connect to database")
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
        runner.logger.info(message=f'Команда {commands[args.command].__name__} успешно выполнена')
        sys.exit(0)
    else:
        runner.logger.fatal(message=f'Команда {commands[args.command].__name__} не выполнена')
        sys.exit(1)


if __name__ == '__main__':
    main()
import sys
import argparse
from src.config import Config
from src.flyway_runner import FlywayRunner


def main():
    parser = argparse.ArgumentParser(description='Database Migration Tool')
    parser.add_argument('command', choices=['migrate', 'info', 'validate', 'clean', 'baseline', 'repair', 'check'],
                        help='Flyway command to execute')
    parser.add_argument('--config', '-c', help='Path to config file')

    args = parser.parse_args()

    # Инициализация конфигурации
    config = Config()
    runner = FlywayRunner(config)

    # Проверка подключения к БД перед выполнением команд
    if not runner.check_connection():
        print("ERROR: Cannot connect to database")
        sys.exit(1)

    # Выполнение команды
    commands = {
        'migrate': runner.migrate,
        'info': runner.info,
        'validate': runner.validate,
        'clean': runner.clean,
        'baseline': runner.baseline,
        'repair': runner.repair,
        'check': runner.check_connection
    }

    success = commands[args.command]()
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
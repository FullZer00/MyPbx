import logging
from datetime import datetime, UTC
from enum import Enum


class CustomLogger:
    def __init__(self, service_name: str):
        self.logger = logging.getLogger(service_name)
        self.service_name = service_name

        if not self.logger.handlers:
            self._setup_logger()

    class LogLevel(Enum):
        INFO = 'INFO',
        DEBUG = 'DEBUG',
        CRITICAL = 'CRITICAL',
        ERROR = 'ERROR',
        FATAL = 'FATAL',
        WARN = 'WARN',
        UNKNOWN = 'UNKNOWN'

    def _setup_logger(self):
        """Настройка формата и обработчиков логгера"""

        # Создаем форматтер для структурированного логирования
        formatter = logging.Formatter(
            fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # Обработчик для вывода в консоль
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        # Добавляем обработчик к логгеру
        self.logger.addHandler(console_handler)

        # Устанавливаем уровень логирования
        self.logger.setLevel(logging.INFO)

        # Предотвращаем дублирование сообщений
        self.logger.propagate = False

    def structured_logger(self,
                          message: str,
                          level: LogLevel = LogLevel.INFO,
                          **kwargs
                          ):
        """Структурированное логирование с дополнительными полями"""

        log_data = {
            "message": message,
            "service": self.service_name,
            "timestamp": datetime.now(UTC).isoformat() + "Z",
            **kwargs
        }

        # В текстовом режиме форматируем красиво
        extra_fields = " ".join([f"{k}={v}" for k, v in kwargs.items()])
        log_message = f"{message} | {extra_fields}" if extra_fields else message
        getattr(self.logger, level.name)(log_message)

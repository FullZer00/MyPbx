import logging
from datetime import datetime, UTC
from enum import Enum
from typing import Any


class CustomLogger:
    def __init__(self, service_name: str) -> None:
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

    def _log(self, level: LogLevel, message: str, **kwargs: Any) -> None:
        """Базовый метод для логирования"""
        extra_fields = " ".join([f"{k}={v}" for k, v in kwargs.items()])
        log_message = f"{message} | {extra_fields}" if extra_fields else message

        log_method = getattr(self.logger, level.name.lower())
        log_method(log_message)

    def info(self, message: str, **kwargs: Any) -> None:
        """Логирование информационного сообщения"""
        self._log(self.LogLevel.INFO, message, **kwargs)

    def error(self, message: str, **kwargs: Any) -> None:
        """Логирование сообщения об ошибке"""
        self._log(self.LogLevel.ERROR, message, **kwargs)

    def warn(self, message: str, **kwargs: Any) -> None:
        """Логирование предупреждения"""
        self._log(self.LogLevel.WARN, message, **kwargs)

    def debug(self, message: str, **kwargs: Any) -> None:
        """Логирование отладочной информации"""
        self._log(self.LogLevel.DEBUG, message, **kwargs)

    def critical(self, message: str, **kwargs: Any) -> None:
        """Логирование критической ошибки"""
        self._log(self.LogLevel.CRITICAL, message, **kwargs)

    def fatal(self, message: str, **kwargs: Any) -> None:
        """Логирование фатальной ошибки"""
        self._log(self.LogLevel.FATAL, message, **kwargs)

    def exception(self, message: str, exception: Exception, **kwargs: Any) -> None:
        """Логирование исключения с трассировкой"""
        extra_fields = " ".join([f"{k}={v}" for k, v in kwargs.items()])
        log_message = f"{message} | {extra_fields}" if extra_fields else message
        self.logger.exception(f"{log_message} | exception={str(exception)}")

    # Методы для установки уровня логирования
    def set_level(self, level: LogLevel) -> None:
        """Установка уровня логирования"""
        level_mapping = {
            self.LogLevel.DEBUG: logging.DEBUG,
            self.LogLevel.INFO: logging.INFO,
            self.LogLevel.WARN: logging.WARNING,
            self.LogLevel.ERROR: logging.ERROR,
            self.LogLevel.CRITICAL: logging.CRITICAL,
            self.LogLevel.FATAL: logging.FATAL,
        }
        self.logger.setLevel(level_mapping.get(level, logging.INFO))

    def enable_debug(self) -> None:
        """Включение отладочного режима"""
        self.set_level(self.LogLevel.DEBUG)

    def disable_debug(self) -> None:
        """Выключение отладочного режима"""
        self.set_level(self.LogLevel.INFO)

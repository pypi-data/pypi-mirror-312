import logging
from typing import Any, Dict, Optional
from colorama import Fore, Style
from . import send_topic_message

class MyLogger:
    def __init__(self, name: str, rabbitmq_config: Optional[Dict[str, Any]] = None, routing_key: Optional[str] = None, 
                 exchange: Optional[str] = None, headers: Optional[Dict[str, Any]] = None):
        """
        Initialize a logger with optional RabbitMQ integration.
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        handler.setFormatter(self._get_color_formatter())
        self.logger.addHandler(handler)

        # RabbitMQ configuration
        self.rabbitmq_config = rabbitmq_config
        self.routing_key = routing_key
        self.exchange = exchange
        self.headers = headers or {}

    def _get_color_formatter(self):
        """
        Formatter with color-coded log levels.
        """
        class ColorFormatter(logging.Formatter):
            COLORS = {
                logging.DEBUG: Fore.CYAN,
                logging.INFO: Fore.GREEN,
                logging.WARNING: Fore.YELLOW,
                logging.ERROR: Fore.RED,
                logging.CRITICAL: Fore.MAGENTA
            }

            def format(self, record):
                color = self.COLORS.get(record.levelno, "")
                record.msg = f"{color}{record.msg}{Style.RESET_ALL}"
                return super().format(record)

        return ColorFormatter('%(asctime)s - %(levelname)s - %(message)s')

    def log(self, level: str, message: str, rabbitmq_message: Optional[str] = None, headers: Optional[Dict[str, Any]] = None):
        """
        Log a message and optionally send it to RabbitMQ.
        """
        log_func = getattr(self.logger, level.lower(), self.logger.info)
        log_func(message)

        # Publish to RabbitMQ if configured
        if self.rabbitmq_config and self.routing_key and self.exchange:
            try:
                send_topic_message(
                    message=rabbitmq_message or message,
                    routing_key=f"logs.{level.lower()}.{self.logger.name}",
                    exchange=self.exchange,
                    config=self.rabbitmq_config,
                    headers={**self.headers, **(headers or {})}
                )
            except Exception as e:
                self.logger.error(f"Failed to send log to RabbitMQ: {e}")

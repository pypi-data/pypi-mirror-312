import logging
import logging.config
import os
from typing import Any, Dict, Optional
from colorama import Fore, Style
from . import send_topic_message

class MyLogger:
    def __init__(self, name, rabbitmq_config=None, routing_key=None, exchange=None, headers: Optional[Dict[str, Any]] = None):
        """
        Initialize the logger using a logging.ini file or default settings.
        
        :param name: Logger name.
        :param logging_ini_path: Path to the logging.ini file.
        :param rabbitmq_config: RabbitMQ configuration.
        :param routing_key: RabbitMQ routing key.
        :param exchange: RabbitMQ exchange name.
        :param headers: RabbitMQ headers.
        """
        self.name = name
        logging_ini_path = os.path.join(os.path.dirname(__file__), "logging.ini")

        # Load logging configuration from ini file
        if logging_ini_path and os.path.exists(logging_ini_path):
            print(f"Loading logging configuration from {logging_ini_path}")
            logging.config.fileConfig(logging_ini_path)
        else:
            logging.basicConfig(level=logging.INFO)  # Fallback to basic config if ini file is not provided

        self.logger = logging.getLogger(name)
        
        # Add color formatter to the console handler
        for handler in self.logger.handlers:
            if isinstance(handler, logging.StreamHandler):
                handler.setFormatter(self._get_color_formatter())
        
        # RabbitMQ configuration
        self.rabbitmq_config = rabbitmq_config
        self.routing_key = routing_key
        self.exchange = exchange
        self.headers = headers or {}

    def _get_color_formatter(self):
        """
        Returns a formatter that adds color to log messages based on the level.
        """
        class ColorFormatter(logging.Formatter):
            level_colors = {
                logging.DEBUG: Fore.CYAN,
                logging.INFO: Fore.GREEN,
                logging.WARNING: Fore.YELLOW,
                logging.ERROR: Fore.RED,
                logging.CRITICAL: Fore.MAGENTA
            }
            reset = Style.RESET_ALL

            def format(self, record):
                color = self.level_colors.get(record.levelno, self.reset)
                record.msg = f"{color}{record.msg}{self.reset}"
                return super().format(record)
        
        return ColorFormatter('%(asctime)s - %(levelname)s - %(message)s')

    def log(self, level, message, rabbitmq_message=None, headers: Optional[Dict[str, Any]] = None):
        """
        Log a message to the console and optionally publish it to RabbitMQ.
        
        :param level: Log level ('info', 'warning', 'error', 'debug', 'critical').
        :param message: Log message to be printed.
        :param rabbitmq_message: Message to be sent to RabbitMQ (if None, `message` is used).
        :param headers: RabbitMQ headers (optional).
        """
        level = level.lower()
        if level == 'info':
            self.logger.info(message)
        elif level == 'warning':
            self.logger.warning(message)
        elif level == 'error':
            self.logger.error(message)
        elif level == 'debug':
            self.logger.debug(message)
        elif level == 'critical':
            self.logger.critical(message)
        else:
            self.logger.log(logging.NOTSET, message)
        
        combined_headers = {**self.headers, **(headers or {})}

        # Publish to RabbitMQ
        if self.rabbitmq_config and self.routing_key and self.exchange:
            try:
                send_topic_message(
                    message=rabbitmq_message or message,
                    routing_key=f"logs.{level}.{self.name}",
                    exchange=self.exchange,
                    config=self.rabbitmq_config,
                    headers=combined_headers
                )
            except Exception as e:
                self.logger.error(f"Failed to send log to RabbitMQ: {e}")

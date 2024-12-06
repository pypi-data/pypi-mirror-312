import logging
from typing import Any, Dict, Optional
from colorama import Fore, Style
from . import send_topic_message

class MyLogger:
    def __init__(self, name, rabbitmq_config=None, level=logging.INFO, routing_key=None, exchange=None, headers: Optional[Dict[str, Any]] = None):
        """
        Initialize the logger.
        
        :param name: Logger name.
        :param rabbitmq_config: RabbitMQ configuration.
        :param level: Logging level.
        :param routing_key: RabbitMQ routing key.
        :param exchange: RabbitMQ exchange name.
        :param headers: RabbitMQ headers.
        """
        self.name = name
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        
        # Console handler with color formatting
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(self._get_color_formatter())
        self.logger.addHandler(console_handler)
        
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
        
        :param level: Log level ('info', 'warning', 'error', 'debug').
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

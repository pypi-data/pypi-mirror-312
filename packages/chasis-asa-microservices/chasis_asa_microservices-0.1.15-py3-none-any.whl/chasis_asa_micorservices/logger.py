import logging
from typing import Any, Dict, Optional
from . import send_topic_message

class MyLogger:
    def __init__(self, name, rabbitmq_config=None, level=logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(console_format)
        self.logger.addHandler(console_handler)
        
        # RabbitMQ configuration
        self.rabbitmq_config = rabbitmq_config

    def log(self, level, message, rabbitmq_message=None, routing_key=None, exchange=None, headers: Optional[Dict[str, Any]] = None):
        """
        Log a message to the console and optionally publish it to RabbitMQ.
        
        :param level: Log level ('info', 'warning', 'error', 'debug').
        :param message: Log message to be printed.
        :param rabbitmq_message: Message to be sent to RabbitMQ (if None, `message` is used).
        :param routing_key: RabbitMQ routing key (required for RabbitMQ logs).
        :param exchange: RabbitMQ exchange name (required for RabbitMQ logs).
        """
        # Log to console
        if level == 'info':
            self.logger.info(message)   
        elif level == 'warning':
            self.logger.warning(message)
        elif level == 'error':
            self.logger.error(message)
        elif level == 'debug':
            self.logger.debug(message)
        else:
            self.logger.log(logging.NOTSET, message)

        # Publish to RabbitMQ
        if self.rabbitmq_config and routing_key and exchange:
            try:
                send_topic_message(
                    message=rabbitmq_message or message,
                    routing_key=routing_key,
                    exchange=exchange,
                    config=self.rabbitmq_config,
                    headers=headers
                )
            except Exception as e:
                self.logger.error(f"Failed to send log to RabbitMQ: {e}")

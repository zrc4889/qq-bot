import sys

from graia.application.logger import AbstractLogger
from loguru import logger


def messagechain_to_img(text, *_):
    return text


class LoguruLogger(AbstractLogger):
    def __init__(self) -> None:
        config = {
            "handlers": [
                {"sink": sys.stdout, "format": "{time:YYYY-MM-DD HH:mm:ss} - {message}"},
                {"sink": 'logs/latest.log', "encoding": 'utf8', "rotation": "12:00",
                 "format": "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | {level} | <level>{message}</level>", "compression": "zip", "enqueue": True},
            ],
            "extra": {"user": "someone"}
        }

        logger.configure(**config)

    def info(self, msg):
        return logger.info(msg)

    def error(self, msg):
        return logger.error(msg)

    def warn(self, msg):
        return logger.warning(msg)

    def exception(self, msg):
        return logger.exception(msg)

    def debug(self, msg):
        return logger.debug(msg)

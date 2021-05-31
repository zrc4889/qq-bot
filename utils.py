'''
Author: nullptr
Date: 2021-05-06 11:59:44
LastEditTime: 2021-05-31 21:40:36
'''
import sys

import yaml
from graia.application.logger import AbstractLogger
from loguru import logger


class Config:
    """
    get config from config.yml
    """
    __instance = None
    __first_init: bool = True

    def __new__(cls, *_):
        if not cls.__instance:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self, arg: str = None):
        if self.__first_init:
            self.config = yaml.safe_load(
                open('config.yml', 'r', encoding='utf-8').read())
            Config.__first_init = False
        self.arg = arg

    def __str__(self):
        return str(self.config)

    def __repr__(self) -> str:
        return self.__str__()

    def get(self, value):
        return self.config[value]

    def save(self):
        if self.config is not None:
            with open('config.yml', 'w', encoding='utf-8') as f:
                yaml.dump(self.config, f)


class LoguruLogger(AbstractLogger):
    def __init__(self, config: dict = None) -> None:
        if config is None:
            config = {
                "handlers": [{
                    "sink": sys.stdout,
                    "format": "{time:YYYY-MM-DD HH:mm:ss} - {message}"
                }]
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

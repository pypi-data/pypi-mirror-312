import enum

from ..exceptions import LibraryException
from ..logging._config import logging_config


class ConfigurationMeta(type):
    def __getitem__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]
        else:
            raise LibraryException(f"Configuration item '{item}' does not exist!")


class Configuration(metaclass=ConfigurationMeta):
    logging = logging_config

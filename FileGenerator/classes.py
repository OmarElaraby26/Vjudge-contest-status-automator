from abc import ABC, ABCMeta, abstractmethod
from random import randint

import json


class SingletonABCMeta(ABCMeta):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class FileGeneratorBasic(object):
    __metaclass__ = SingletonABCMeta

    def _get_full_path(self, path, file_name):
        if path[-1] != '/':
            path += '/'

        if file_name == "":
            file_name = str(randint(10000, 99999))

        return path + file_name

    @abstractmethod
    def generate(self, data, path, file_name):
        pass


class TextFileGenerator(FileGeneratorBasic):
    def generate(self, data, path, file_name):
        full_path = self._get_full_path(path, file_name) + '.txt'
        json.dump(data, open(full_path, 'w'),  sort_keys=True, indent=4)

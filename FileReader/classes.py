import json


class BasicFileReaderMeta(type):
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


class BasicFileReader(metaclass=BasicFileReaderMeta):
    def read_file_as_string(self, file_path):
        f = open(file_path, "r")
        return f.read()

    def read(self, file_path):
        pass


class JsonFileReader(BasicFileReader):
    def __init__(self):
        super().__init__()

    def read(self, file_path):
        content = self.read_file_as_string(file_path)
        # todo: error handling
        # if content is not json structure
        return dict(json.loads(content))

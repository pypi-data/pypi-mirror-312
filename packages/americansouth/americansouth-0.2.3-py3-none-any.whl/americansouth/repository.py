import abc
import json
import typing


class Repository(abc.ABC):
    @abc.abstractmethod
    def load(self) -> typing.List[typing.Dict[str, typing.Any]]:
        pass


class JsonRepository(Repository):
    def __init__(self, data_file: str) -> None:
        self.data_file = data_file

    def load(self) -> typing.List[typing.Dict[str, typing.Any]]:
        with open(self.data_file) as f:
            return json.load(f)

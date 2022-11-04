from abc import ABC, abstractmethod

import numpy


class Visitor:
    """Посетитель, который будет посещать различные объекты и получать данные
    для графиков"""

    _x_data = []  # TODO: научиться принимать значения в visitor
    _y_data = []
    _legends = []
    _x_label = None
    _y_label = None
    _types = None
    _file_name = None

    def visit(self, obj) -> None:
        obj.accept(self)

    @property
    def data(self) -> (list[numpy.ndarray], list[numpy.ndarray]):
        return self._x_data, self._y_data

    @property
    def legends(self) -> list[str]:
        return self._legends

    @property
    def labels(self) -> (str, str):
        return self._x_label, self._y_label

    @property
    def types(self) -> list[str]:
        return self._types

    @property
    def file_name(self) -> str:
        return self._file_name


class Worker(ABC):
    """Абстрактный класс для посещения Visitor"""

    @abstractmethod
    def accept(self, visitor: Visitor) -> None:
        pass

from abc import ABC, abstractmethod
from pydantic import BaseModel, validate_arguments
import numpy


class Worker(ABC):
    """Абстрактный класс для посещения Visitor"""

    @abstractmethod
    def accept(self, visitor) -> None:
        pass


class Visitor(BaseModel):
    """Посетитель, который будет посещать различные объекты и получать данные
    для графиков"""
    _x_data: list[numpy.ndarray]
    # TODO: научиться принимать значения в visitor
    _y_data: list[numpy.ndarray]
    _legends: list[str]
    _x_label: str
    _y_label: str
    _types: list[str]
    _file_name: str
    _current_predicted_y_data: numpy.ndarray

    @validate_arguments
    def visit(self, obj: Worker) -> None:
        obj.accept(self)

    @property
    def data(self) -> (list[numpy.ndarray], list[numpy.ndarray]):
        return self._x_data, self._y_data

    @data.setter
    def data(self, p: tuple[list[numpy.ndarray], list[numpy.ndarray]]):
        self._x_data, self._y_data = p

    @property
    def legends(self) -> list[str]:
        return self._legends

    @legends.setter
    def legends(self, val: str):
        self._legends.append(val)

    @property
    def labels(self) -> (str, str):
        return self._x_label, self._y_label

    @labels.setter
    def labels(self, val: tuple[str, str]):
        self._x_label, self._y_label = val

    @property
    def types(self) -> list[str]:
        return self._types

    @types.setter
    def types(self, val: list[str]):
        self._types = val

    @property
    def file_name_to_write_data(self) -> str:
        return self._file_name

    @file_name_to_write_data.setter
    def file_name_to_write_data(self, val: str):
        self._file_name = val

    @property
    def current_predicted_y_data(self):
        return self._current_predicted_y_data

    @current_predicted_y_data.setter
    def current_predicted_y_data(self, value: numpy.ndarray):
        self._current_predicted_y_data = value

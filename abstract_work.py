from abc import ABC, abstractmethod
import numpy


class Worker(ABC):
    """Абстрактный класс для посещения Visitor"""

    @abstractmethod
    def accept(self, visitor) -> None:
        pass


class Visitor:
    """Посетитель, который будет посещать различные объекты и получать данные
    для графиков"""

    def __init__(self):
        self.data = ([], [])
        self.types = []
        self.legends = []
        self.types_of_interpolation = []
        self.labels = ('', '')
        self.file_name_to_write_data = None
        self.show = True
        self.current_predicted_y_data = []
        self.x_ranges = []
        self.degrees = []

    def visit(self, obj: Worker) -> None:
        obj.accept(self)

    @property
    def data(self) -> (list[numpy.array], list[numpy.array]):
        return self._x_data, self._y_data

    @data.setter
    def data(self, p: tuple[list[numpy.array], list[numpy.array]]):
        self._x_data, self._y_data = p

    @property
    def legends(self) -> list[str]:
        return self._legends

    @legends.setter
    def legends(self, val: list[str]):
        self._legends = val

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
    def current_predicted_y_data(self, value):
        self._current_predicted_y_data = value

    @property
    def show(self):
        return self._show

    @show.setter
    def show(self, value):
        self._show = value

    @property
    def types_of_interpolation(self):
        return self._types_of_interpolation

    @types_of_interpolation.setter
    def types_of_interpolation(self, value):
        self._types_of_interpolation = value

    @property
    def x_ranges(self):
        return self._x_ranges

    @x_ranges.setter
    def x_ranges(self, value):
        self._x_ranges = value

    @property
    def degrees(self):
        return self._degrees

    @degrees.setter
    def degrees(self, value):
        self._degrees = value

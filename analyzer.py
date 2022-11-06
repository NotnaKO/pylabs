import numpy

from abstract_work import Worker, Visitor
from pydantic import validate_arguments
from sklearn import linear_model, preprocessing


class Analyzer(Worker):
    """Класс, который анализирует данные и создаёт модели аппроксимаций"""

    # TODO: добавить видов интерполяций
    _allowed_types = {"linear", "polynomial", "any"}

    def _check(self, type_of_interpolation) -> None:
        if type_of_interpolation is not None and (
                type_of_interpolation not in self._allowed_types):
            raise ValueError(f"""We do not support this type of 
            interpolation. Please choice one of allowed types: 
            {', '.join(self._allowed_types)}""")

    @validate_arguments
    def __init__(self, type_of_interpolation: str = None,
                 x_range: numpy.ndarray = None):
        self._check(type_of_interpolation)
        self._type_of_interpolation = type_of_interpolation
        self._x_range = x_range

    @property
    def type_of_interpolation(self):
        return self._type_of_interpolation

    @type_of_interpolation.setter
    def type_of_interpolation(self, value):
        self._check(type_of_interpolation=value)
        self._type_of_interpolation = value

    @property
    def x_range(self):
        return self._x_range

    @x_range.setter
    @validate_arguments
    def x_range(self, value: numpy.ndarray):
        self._x_range = value

    @validate_arguments
    def accept(self, visitor: Visitor, index: int) -> None:
        if self._type_of_interpolation is None:
            return
        x_data, y_data = visitor.data
        x_raw = x_data[index]
        x_raw.reshape((-1, 1))
        y_raw = y_data[index]
        x_range_copy = self._x_range
        x_range_copy.reshape((-1, 1))
        match self._type_of_interpolation:
            case "linear":
                model = linear_model.LinearRegression().fit(x_raw, y_raw)
                print(f"Score of the data: {model.score(x_raw, y_raw)}")
                print(f"""Intercept: {model.intercept_}
                Coefficient: {model.coef_[0]}""")
                visitor.current_predicted_y_data = model.predict(x_range_copy)
            case "polynomial":
                pass

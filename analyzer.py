import numpy

from abstract_work import Worker, Visitor
from pydantic import validate_arguments
from scipy.interpolate import Akima1DInterpolator
from sklearn import linear_model, preprocessing


class Analyzer(Worker):
    """Класс, который анализирует данные и создаёт модели аппроксимаций"""

    _allowed_types = {"linear", "polynomial", "any"}

    def _check(self, type_of_interpolation) -> None:
        if type_of_interpolation is not None and (type_of_interpolation not in self._allowed_types):
            raise ValueError(f"""We do not support this type of 
            interpolation. Please choice one of allowed types: 
            {', '.join(self._allowed_types)}""")

    @validate_arguments
    def __init__(self, type_of_interpolation: list[str] | None = None,
                 degrees: list[int] | None = None, x_range: list | None = None):
        self._check(type_of_interpolation)
        self._type_of_interpolation = type_of_interpolation
        self._degree = degrees
        self._x_range = x_range

    @property
    def type_of_interpolation(self):
        return self._type_of_interpolation

    @type_of_interpolation.setter
    def type_of_interpolation(self, value):
        self._check(type_of_interpolation=value)
        self._type_of_interpolation = value

    @property
    def degree(self):
        return self._degree

    @degree.setter
    @validate_arguments
    def degree(self, value: int):
        self._degree = value

    @property
    def x_range(self) -> numpy.array:
        return self._x_range

    @x_range.setter
    def x_range(self, value: numpy.array):
        self._x_range = value

    @staticmethod
    def _print_model_information(model, x_raw, y_raw, index):
        print(f"The data number {index}:")
        print(f"Score of the data: "
              f"{model.score(x_raw, y_raw)}")
        print(f"""Intercept: {round(model.intercept_, 9)}.\n Coefficients:""")
        for i, j in enumerate(model.coef_):
            print(i, round(j, 9))

    def accept(self, visitor: Visitor) -> None:
        for index in range(len(visitor.data[0])):
            if visitor.types_of_interpolation[index] is None:
                continue
            x_data, y_data = visitor.data
            x_raw = x_data[index]
            y_raw = y_data[index]
            x_range_copy = visitor.x_ranges[index]
            if x_range_copy is None:
                x_range_copy = numpy.linspace(min(x_raw), max(x_raw), 100)
                visitor.x_ranges[index] = x_range_copy
            match visitor.types_of_interpolation[index]:
                case "linear":
                    model = linear_model.LinearRegression().fit(x_raw.reshape((-1, 1)), y_raw)
                    self._print_model_information(model, x_raw.reshape(-1, 1), y_raw, index)
                    visitor.current_predicted_y_data.append(
                        model.predict(x_range_copy.reshape((-1, 1))))

                case "polynomial":
                    poly = preprocessing.PolynomialFeatures(
                        degree=visitor.degrees[index] if visitor.degrees[index] is not None else 4)
                    x_poly = poly.fit_transform(x_raw.reshape((-1, 1)))
                    poly.fit(x_poly, y_raw)
                    model = linear_model.LinearRegression().fit(x_poly, y_raw)
                    self._print_model_information(model, x_poly, y_raw, index)
                    visitor.current_predicted_y_data.append(
                        model.predict(poly.fit_transform(x_range_copy.reshape(-1, 1))))
                case "any":
                    model = Akima1DInterpolator(x_raw, y_raw)
                    result = model(x_range_copy)
                    visitor.current_predicted_y_data.append(result)

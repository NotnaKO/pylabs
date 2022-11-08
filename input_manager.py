import numpy
from abstract_work import Worker
from os.path import exists
from pydantic import validate_arguments


class InputManager(Worker):
    """Класс, который собирает информацию от пользователя и передает её
    Visitor"""

    _x_data = []
    _x_range = None
    _y_data = []
    _label = []
    _x_label = None
    _y_label = None
    _type = None
    _type_of_interpolation = None
    _file_name = None
    _file_name_to_save_figure = None
    _show = True
    _input_data_type = float
    _degree = None
    _types_of_interpolations = {"any", "linear", "polynomial", None}
    _x_error = None
    _y_error = None
    _error_label = None

    @staticmethod
    def _find_file(path: str, extension: str):
        if exists(path):
            return path
        if exists(path + extension):
            return path + extension
        raise FileNotFoundError("No such file in directory")

    @validate_arguments
    def __init__(self, *args, input_type: str | None = None, input_file_name: str | None = None,
                 input_data_type=float, separator: str | None = None, show: bool = True, **kwargs):
        self.read_data(*args, input_type=input_type, input_file_name=input_file_name,
                       input_data_type=input_data_type, separator=separator, show=show, **kwargs)

    def _fill_argument(self, key, value):
        match key:
            case "label":
                self._label = value
            case "x_label":
                self._x_label = value
            case "y_label":
                self._y_label = value
            case "file_name_to_save_figure":
                self._file_name_to_save_figure = value
            case "input_data_type":
                self._input_data_type = value
            case "x_range":
                self._x_range = value
            case "degree":
                self._degree = value
            case "x_error":
                self._x_error = value
            case "y_error":
                self._y_error = value
            case "error_label":
                self._error_label = value
            case "type":
                self._type = value
            case "type_of_interpolation":
                if value.lower() not in self._types_of_interpolations:
                    raise ValueError("Type of interpolation may be only "
                                     "\"any\", \"linear\", \"polynomial\" "
                                     "or None")
                self._type_of_interpolation = value
            case _:
                raise AttributeError(f"Pylab has not got attribute \"{key}\". Allowed "
                                     f"attributes: label, x_label, y_label, file_name_to_plot, "
                                     f"type_of_interpolation, x_error, y_error, error_label, type "
                                     f"and input_data_type")

    def read_data(self, *args, input_type: str, input_file_name: str, input_data_type,
                  separator: str, show: bool, **kwargs):
        self._show = show
        match input_type:
            case "stdin":
                self._x_data = list(map(input_data_type, input("Введите данные по x через "
                                                               "пробел: \n")))
                self._y_data = list(map(input_data_type, input("Введите данные по у через "
                                                               "пробел: \n")))

                self._label = input("Введите название функции(пустую "
                                    "строку, если её нет) \n")
                if self._label == '':
                    self._label = None
                self._x_label = input("Введите название название оси абсцисс(пустую строку, "
                                      "если её нет) \n")
                if self._x_label == '':
                    self._x_label = None
                self._y_label = input("Введите название оси ординат(пустую строку, если её "
                                      "нет) \n")
                if self._y_label == '':
                    self._y_label = None
                self._file_name_to_save_figure = input(
                    "Введите название файла  для записи(пустую строку, "
                    "если её нет) \n")
                if self._file_name_to_save_figure == '':
                    self._file_name_to_save_figure = None
                s = f"Введите тип интерполяции(возможные типы: " \
                    f"{', '.join(self._types_of_interpolations)})\n"
                self._type_of_interpolation = input(s)
                if self._type_of_interpolation == "None":
                    self._type_of_interpolation = None
                if self._type_of_interpolation not in self._types_of_interpolations:
                    raise ValueError("Type of interpolation may be only "
                                     "\"any\", \"linear\", \"polynomial\" "
                                     "or None")
                if self._type_of_interpolation == "polynomial":
                    self._degree = input("Введите степень полинома для аппроксимации\n")
                    self._degree = int(self._degree)
                    if self._degree < 0:
                        raise ValueError("Degree must be non-negative integer")
                else:
                    self._degree = None
                self._show = (input("Показывать график?(Да, Нет)\n") == "Да")
                if input("Хотите написать диапазон для x?(Да, Нет(будет посчитан "
                         "автоматически))") == "Да":
                    start = float(input("Введите начальный x"))
                    end = float(input("Введите конечный x"))
                    step = float(input("Введите шаг"))
                    self._x_range = numpy.linspace(start, end, int((end - start) // step))
                else:
                    self._x_range = None
            case ".txt":
                input_file_name = self._find_file(input_file_name, '.txt')
                with open(input_file_name) as f:
                    lines = f.readlines()
                self._x_data = list(map(input_data_type, lines[0].split(separator)))
                self._y_data = list(map(input_data_type, lines[1].split(separator)))
                for i in lines[2:]:
                    cmd, value = i.split(':')
                    self._fill_argument(cmd, value)
            case _:
                self._x_data = args[0]
                self._y_data = args[1]
                for key, value in kwargs.items():
                    self._fill_argument(key, value)

    def accept(self, visitor) -> None:
        x, y = visitor.data
        x.append(numpy.array(self._x_data, dtype=self._input_data_type))
        y.append(numpy.array(self._y_data, dtype=self._input_data_type))
        visitor.legends.append(self._label)
        visitor.labels = (self._x_label, self._y_label)
        visitor.types.append(self._type)
        visitor.show = self._show
        visitor.types_of_interpolation.append(self._type_of_interpolation)
        visitor.x_ranges.append(self._x_range)
        visitor.degrees.append(self._degree)
        visitor.x_error.append(self._x_error)
        visitor.y_error.append(self._y_error)
        visitor.error_labels.append(self._error_label)
        if self._file_name_to_save_figure is not None:
            visitor.file_name_to_write_data = self._file_name_to_save_figure

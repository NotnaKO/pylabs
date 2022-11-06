import numpy

from abstract_work import Worker, Visitor
from pydantic import validate_arguments
from os.path import exists


class InputManager(Worker):
    """Класс, который собирает информацию от пользователя и передает её
    Visitor"""

    _x_data = []
    _y_data = []
    _legend = []
    _x_label = None
    _y_label = None
    _type = None
    _file_name = None
    _file_name_to_write = None

    @staticmethod
    def _find_file(path: str, extension: str):
        if exists(path):
            return path
        if exists(path + extension):
            return path + extension
        raise FileNotFoundError("No such file in directory")

    @validate_arguments
    def __init__(self, input_type: str = "stdin", input_file_name: str = '',
                 input_data_type=float, separator: str = ' ',
                 legend_line: int = None, x_label_line: int = None,
                 y_label_line: int = None,
                 file_name_to_write_line: int = None):
        self.read_data(input_type, input_file_name, input_data_type, separator,
                       legend_line, x_label_line, y_label_line,
                       file_name_to_write_line)

    @validate_arguments
    def read_data(self, input_type: str = "stdin", input_file_name: str = '',
                  input_data_type=float, separator: str = ' ',
                  legend_line: int = None, x_label_line: int = None,
                  y_label_line: int = None,
                  file_name_to_write_line: int = None):
        match input_type:
            case "stdin":
                self._x_data = list(map(input_data_type, input("""Введите 
                        данные по x: \n
                        """)))
                self._y_data = list(map(input_data_type, input("""Введите 
                        данные по у: \n
                        """)))
                if legend_line is not None:
                    self._legend = input("""Введите название функции(пустую 
                            строку, если её нет) \n
                            """)
                    if self._legend == '':
                        self._legend = None
                if x_label_line is not None:
                    self._x_label = input("""Введите название название оси 
                            абсцисс(пустую строку, если её нет) \n
                            """)
                    if self._x_label == '':
                        self._x_label = None
                if y_label_line is not None:
                    self._y_label = input("""Введите название оси ординат(
                            пустую строку, если её нет) \n
                            """)
                    if self._y_label == '':
                        self._y_label = None
                if file_name_to_write_line is not None:
                    self._file_name_to_write = input("""Введите название файла 
                            для записи(пустую строку, если её нет) \n
                            """)
                    if self._file_name_to_write == '':
                        self._file_name_to_write = None
            case ".txt":
                input_file_name = self._find_file(input_file_name, '.txt')
                with open(input_file_name) as f:
                    lines = f.readlines()
                self._x_data = list(
                    map(input_data_type, lines[0].split(separator)))
                self._y_data = list(
                    map(input_data_type, lines[1].split(separator)))
                if legend_line is not None:
                    self._legend = lines[legend_line]
                if x_label_line is not None:
                    self._x_label = lines[x_label_line]
                if y_label_line is not None:
                    self._y_label = lines[y_label_line]
                if file_name_to_write_line is not None:
                    self._file_name_to_write = lines[file_name_to_write_line]

    @validate_arguments
    def accept(self, visitor: Visitor) -> None:
        x, y = visitor.data
        x.append(numpy.ndarray(self._x_data))
        y.append(numpy.ndarray(self._y_data))
        visitor.legends.append(self._legend)
        x, y = visitor.labels
        x.append(self._x_label)
        y.append(self._y_label)
        visitor.types.append(self._type)
        if self._file_name_to_write is not None:
            visitor.file_name_to_write_data = self._file_name_to_write

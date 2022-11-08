from abstract_work import Visitor
from input_manager import InputManager
from analyzer import Analyzer
from plotter import Plotter


class Pylab:
    """Класс для работы с пользователем"""

    def __init__(self, *args, **kwargs):
        """Функция создаёт график по параметрам"""
        self.__visitor = Visitor()
        self.add(*args, **kwargs)

    def work(self):
        analyzer = Analyzer()
        self.__visitor.visit(analyzer)
        plotter = Plotter()
        self.__visitor.visit(plotter)

    def add(self, *args, **kwargs):
        """Функция добавляет график по параметрам"""
        inp = InputManager(*args, **kwargs)
        self.__visitor.visit(inp)

from abstract_work import Visitor
from input_manager import InputManager
from analyzer import Analyzer
from plotter import Plotter


class ClientWorker:
    def __init__(self, *args, **kwargs):
        self.__visitor = Visitor()
        inp = InputManager(*args, **kwargs)
        self.__visitor.visit(inp)

    def work(self):
        analyzer = Analyzer()

        self.__visitor.visit(analyzer)
        plotter = Plotter()
        self.__visitor.visit(plotter)


Pylab = ClientWorker

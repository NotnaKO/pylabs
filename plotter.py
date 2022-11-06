from abstract_work import Worker, Visitor
from matplotlib.pylab import *


class Plotter(Worker):
    def __init__(self):
        self._x_label = []
        self._y_label = []
        self._x_data = []
        self._y_data = []

    def accept(self, visitor: Visitor) -> None:
        self._x_data, self._y_data = visitor.data
        self._x_label, self._y_label = visitor.labels
        for i in range(len(self._x_data)):
            current_type = visitor.types[i]
            xlabel(self._x_label)
            ylabel(self._y_label)
            match current_type:
                case "scatter":
                    scatter(self._x_data[i], self._y_data[i],
                            legend=visitor.legends[i])

                    # TODO: дописать различных типов графиков
                case _:
                    plot(self._x_data[i], self._y_data[i],
                         legend=visitor.legends[i])
        savefig(visitor.file_name_to_write_data)

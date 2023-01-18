from abstract_work import Worker, Visitor
from matplotlib.pylab import xlabel, ylabel, scatter, plot, legend, savefig, show, errorbar, grid


class Plotter(Worker):
    """Класс, строящий графики"""

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
            grid(True)
            match current_type:
                case "scatter":
                    if visitor.x_error[i] is None and visitor.y_error[i] is None:
                        scatter(self._x_data[i], self._y_data[i],
                                label=visitor.legends[i] if visitor.types_of_interpolation[
                                                                i] is None else None)
                    else:
                        label = visitor.error_labels[i]
                        if visitor.types_of_interpolation[i] is None and label is None:
                            label = visitor.legends[i]
                        errorbar(self._x_data[i], self._y_data[i], xerr=visitor.x_error[i],
                                 yerr=visitor.y_error[i], label=label, fmt='o', capsize=3)
                    if visitor.types_of_interpolation[i] is not None:
                        plot(visitor.x_ranges[i], visitor.current_predicted_y_data[i],
                             label=visitor.legends[i])
                case _:
                    plot(self._x_data[i], self._y_data[i], label=visitor.legends[i])
        legend()
        if visitor.file_name_to_write_data:
            savefig(visitor.file_name_to_write_data)
        if visitor.show:
            show()

import numpy
from client_worker import Pylab


def example():
    # Example
    x_data = numpy.linspace(1, 20, 20)
    y_data = numpy.sin(x_data) * x_data
    lab = Pylab(x_data, y_data, label=r"$y_1(x)(linear)$", type="scatter",
                type_of_interpolation="linear",
                file_name_to_save_figure="a.png", y_error=1, x_error=0.5,
                error_label="data with errors")
    lab.add(x_data, y_data, label=r"$y_2(x)(polynomial \ with\ degree=5)$",
            type="scatter", type_of_interpolation="polynomial", degree=5)
    lab.add(x_data, y_data, label=r"$y_3(x)(any)$", type="scatter",
            type_of_interpolation="any")
    lab.work()


if __name__ == '__main__':
    lab = Pylab("stdin")
    lab.work()

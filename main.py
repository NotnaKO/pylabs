import numpy
from client_worker import Pylab

if __name__ == '__main__':
    # Example
    x_data = numpy.linspace(1, 20, 20)
    y_data = numpy.sin(x_data)
    lab = Pylab(x_data, y_data, label=r"$y_1(x)(linear)$", type="scatter",
                type_of_interpolation="linear", file_name_to_save_figure="a.png", y_error=0.1,
                x_error=0.1)
    lab.add(x_data, y_data, label=r"$y_2(x)(polynomial)$", type="scatter",
            type_of_interpolation="polynomial", degree=5)
    lab.add(x_data, y_data, label=r"$y_3(x)(any)$", type="scatter", type_of_interpolation="any")
    lab.work()

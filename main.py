import numpy

from client_worker import Pylab

x_data = [i for i in range(1, 100)]
y_data = [numpy.log(i) for i in x_data]
lab = Pylab(x_data, y_data, legend=r"y(x)", type_of_interpolation="any",
            type="scatter", file_name_to_save_figure="a.png")
lab.work()

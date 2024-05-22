import numpy


class Compensator:
    def __init__(self, file):
        self.table = numpy.loadtxt(file, delimiter=',', skiprows=1)

    def compensate(self, meas):
        return numpy.interp(meas, self.table[:, 0], self.table[:, 1])

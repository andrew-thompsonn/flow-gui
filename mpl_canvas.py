import sys
import matplotlib
matplotlib.use('Qt5Agg')

from PyQt5 import QtCore, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        fig.patch.set_facecolor('black')
        #fig.setStyleSheet("background-color:black")
        self.axes = fig.add_subplot(111)
        self.axes.set_facecolor('black')
        super(MplCanvas, self).__init__(fig)
        self.setStyleSheet('background-color:black')

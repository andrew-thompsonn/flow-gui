from PyQt5.QtWidgets import QMainWindow, QWidget
from PyQt5.QtGui import  QImage, QPalette, QBrush, QIcon
from PyQt5.QtCore import QSize

from central_widget import CentralWidget

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setStyleSheet("background-color: rgb(20, 20, 20);")
        self.setFixedSize(700,800)

        # Add a menu bar
        menuBar = self.menuBar()
        # Make it sexy
        menuBar.setStyleSheet("background:grey;")

        # File menu
        fileMenu = menuBar.addMenu("File")
        # File/Load
        loadAction = fileMenu.addAction("Load")

        centralWidget = CentralWidget()
        self.setCentralWidget(centralWidget)

        self.setWindowTitle("NACA AIRFOIL TOOLS")

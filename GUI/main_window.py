from PyQt5.QtWidgets import QMainWindow, QWidget
# from PyQt5.QtGui import  QImage, QPalette, QBrush, QIcon
# from PyQt5.QtCore import QSize

from GUI.central_widget import CentralWidget

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setStyleSheet("background-color: rgb(20, 20, 20);")
        self.setFixedSize(1400, 800)

        menuBar = self.menuBar()
        menuBar.setStyleSheet("background-color:rgb(60, 60, 60);")


        centralWidget = CentralWidget()
        self.setCentralWidget(centralWidget)

        self.setWindowTitle("")

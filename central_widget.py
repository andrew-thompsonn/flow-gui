from PyQt5.QtWidgets import QWidget, QDialog, QStackedWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QComboBox, QSlider
from PyQt5.QtGui import QIcon, QFont, QImage, QPalette, QBrush
from PyQt5.QtCore import QSize, Qt, pyqtSignal

from mpl_canvas import MplCanvas
from NACA_4_Digit import Naca4Digit

import numpy as np


class CentralWidget(QWidget):
################################################################################
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        naca0012 = Naca4Digit(0, 0, 0.12, 2, 100)
        print(type(naca0012))
        self.naca0012 = None

        # Main Figure
        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        self.m = 0
        self.p = 0
        self.c = 0
        self.t = 0

        #-----------------------------------------------------------------------
        # LAYOUTS
        #-----------------------------------------------------------------------
        mainLayout = QVBoxLayout(self)
        # Title
        titleLayout = QVBoxLayout()
        titleLayout.setAlignment(Qt.AlignTop)
        # Main figure
        figureLayout = QHBoxLayout()
        figureLayout.setContentsMargins(30, 75, 30, 75)
        # Sliders
        sliderLayout = QVBoxLayout()
        # AoA slider
        alphaSliderLayout = QVBoxLayout()
        alphaSliderLayout.setContentsMargins(25, 15, 40, 15)
        # Velocity slider
        velocitySliderLayout = QVBoxLayout()
        velocitySliderLayout.setContentsMargins(25, 15, 40, 15)

        airfoilOptionsLayout = QVBoxLayout()
        airfoilOptionsLayout.setContentsMargins(40, 15, 65, 100)
        camberLayout = QHBoxLayout()
        camberLocationLayout = QHBoxLayout()
        airfoilThicknessLayout = QHBoxLayout()
        chordLayout = QHBoxLayout()

        parametersLayout = QHBoxLayout()

        #-----------------------------------------------------------------------
        # WIDGETS
        #-----------------------------------------------------------------------
        # Title Label
        titleLabel = QLabel("Airfoil Tools")
        titleLabel.setFixedHeight(80)
        titleLabel.setFont(QFont("Serif", 20))
        titleLabel.setStyleSheet("color:white;")

        # AoA slider & Label
        alphaSlider = QSlider(Qt.Horizontal)
        alphaSlider.setMinimum(-5)
        alphaSlider.setMaximum(10)
        alphaSlider.setTickInterval(30)
        self.alphaSliderLabel = QLabel("Angle of Attack")
        self.alphaSliderLabel.setAlignment(Qt.AlignCenter)
        self.alphaSliderLabel.setFont(QFont("Serif", 10))
        self.alphaSliderLabel.setStyleSheet("color:white;")

        # Velocity slider & Label
        velocitySlider = QSlider(Qt.Horizontal)
        velocitySlider.setMinimum(10)
        velocitySlider.setMaximum(100)
        velocitySlider.setTickInterval(100)
        self.velocitySliderLabel = QLabel("Velocity [m/s]")
        self.velocitySliderLabel.setAlignment(Qt.AlignCenter)
        self.velocitySliderLabel.setFont(QFont("Serif", 10))
        self.velocitySliderLabel.setStyleSheet("color:white;")

        # Combo box for camber value & label
        camberValues = np.linspace(0, 100, 101)
        self.camberValues = [str(c) for c in camberValues]
        camberComboBox = QComboBox()
        camberComboBox.addItems(self.camberValues)
        camberComboBox.setFixedSize(70, 25)
        camberComboBox.setStyleSheet("color:white;")
        camberLabel = QLabel("Camber                  ")
        camberLabel.setFont(QFont("serif", 10))
        camberLabel.setStyleSheet("color:white;")

        # Combo box for camber location & label
        camberLocationValues = np.linspace(0, 10, 11)
        self.camberLocationValues = [str(c) for c in camberLocationValues]
        camberLocationComboBox = QComboBox()
        camberLocationComboBox.addItems(self.camberLocationValues)
        camberLocationComboBox.setFixedSize(70, 25)
        camberLocationComboBox.setStyleSheet("color:white;")
        camberLocationLabel = QLabel("Camber Location        ")
        camberLocationLabel.setFont(QFont("serif", 10))
        camberLocationLabel.setStyleSheet("color:white;")

        # Combo box for airfoil thickness & label
        airfoilThicknessValues = np.linspace(0, 40, 41)
        self.airfoilThicknessValues = [str(t) for t in airfoilThicknessValues]
        airfoilThicknessComboBox = QComboBox()
        airfoilThicknessComboBox.addItems(self.airfoilThicknessValues)
        airfoilThicknessComboBox.setFixedSize(70, 25)
        airfoilThicknessComboBox.setStyleSheet("color:white;")
        airfoilThicknessLabel = QLabel("Airfoil Thickness      ")
        airfoilThicknessLabel.setFont(QFont("serif", 10))
        airfoilThicknessLabel.setStyleSheet("color:white;")

        chordValues = np.linspace(0, 40, 41)
        self.chordValues = [str(t) for t in airfoilThicknessValues]
        chordComboBox = QComboBox()
        chordComboBox.addItems(self.airfoilThicknessValues)
        chordComboBox.setFixedSize(70, 25)
        chordComboBox.setStyleSheet("color:white;")
        chordLabel = QLabel("Chord Length        ")
        chordLabel.setFont(QFont("serif", 10))
        chordLabel.setStyleSheet("color:white;")

        plotButton = QPushButton("Plot Airfoil")
        plotButton.setStyleSheet("color:White;")

        #-----------------------------------------------------------------------
        # LAYOUT MANAGEMENT
        #-----------------------------------------------------------------------
        titleLayout.addWidget(titleLabel)
        figureLayout.addWidget(self.canvas)

        camberLayout.addWidget(camberLabel)
        camberLayout.addWidget(camberComboBox)
        camberLocationLayout.addWidget(camberLocationLabel)
        camberLocationLayout.addWidget(camberLocationComboBox)
        airfoilThicknessLayout.addWidget(airfoilThicknessLabel)
        airfoilThicknessLayout.addWidget(airfoilThicknessComboBox)
        chordLayout.addWidget(chordLabel)
        chordLayout.addWidget(chordComboBox)

        airfoilOptionsLayout.addLayout(camberLayout)
        airfoilOptionsLayout.addLayout(camberLocationLayout)
        airfoilOptionsLayout.addLayout(airfoilThicknessLayout)
        airfoilOptionsLayout.addLayout(chordLayout)
        airfoilOptionsLayout.addWidget(plotButton)

        alphaSliderLayout.addWidget(alphaSlider)
        alphaSliderLayout.addWidget(self.alphaSliderLabel)
        velocitySliderLayout.addWidget(velocitySlider)
        velocitySliderLayout.addWidget(self.velocitySliderLabel)

        sliderLayout.addLayout(alphaSliderLayout)
        sliderLayout.addLayout(velocitySliderLayout)

        parametersLayout.addLayout(airfoilOptionsLayout)
        parametersLayout.addLayout(sliderLayout)

        mainLayout.addLayout(figureLayout)
        mainLayout.addLayout(parametersLayout)

        #-----------------------------------------------------------------------
        # LAYOUT MANAGEMENT
        #-----------------------------------------------------------------------
        alphaSlider.valueChanged.connect(self.alphaChanged)
        velocitySlider.valueChanged.connect(self.velocityChanged)
        plotButton.clicked.connect(self.setAirfoil)

        camberComboBox.currentIndexChanged.connect(self.setCamber)
        camberLocationComboBox.currentIndexChanged.connect(self.setCamberLocation)
        airfoilThicknessComboBox.currentIndexChanged.connect(self.setThickness)
        chordComboBox.currentIndexChanged.connect(self.setChord)

        #-----------------------------------------------------------------------
        # END GRAPHICS
        #-----------------------------------------------------------------------

################################################################################
    def alphaChanged(self, value):
        self.alphaSliderLabel.setText("Angle of Attack: {} deg".format(str(value)))

################################################################################
    def velocityChanged(self, value):
        self.velocitySliderLabel.setText("Velocity: {} [m/s]".format(str(value)))

################################################################################
    def setCamber(self, camberIndex):
        self.m = int(float(self.camberValues[camberIndex]))/100

################################################################################
    def setCamberLocation(self, camberLocationIndex):
        self.p = int(float(self.camberLocationValues[camberLocationIndex]))/10

################################################################################
    def setThickness(self, thicknessIndex):
        self.t = int(float(self.airfoilThicknessValues[thicknessIndex]))/100

################################################################################
    def setChord(self, chordIndex):
        self.c = int(float(self.chordValues[chordIndex]))

################################################################################
    def showFigure(self, airfoil):
        xPts, yPts = airfoil.calculateAirfoilBorder()
        self.canvas.axes.cla()
        airfoil.plotAirfoil(xPts,yPts,self.canvas)
        self.canvas.draw()

################################################################################
    def setAirfoil(self):
        airfoil = Naca4Digit(self.m, self.p, self.t, self.c, 100)
        self.showFigure(airfoil)

################################################################################

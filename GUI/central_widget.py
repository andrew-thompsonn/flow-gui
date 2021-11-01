from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox, QSlider, QPlainTextEdit
from PyQt5.QtGui import QFont

from GUI.mpl_canvas import MplCanvas
from CFD.NACA_4_Digit import Naca4Digit

import numpy as np


class CentralWidget(QWidget):
    def __init__(self, *args, **kwargs):
        """ Initialize parent class, load default airfoil, organize all layouts, connect signals """
        super().__init__(*args, **kwargs)

        # Main Figure
        self.primaryCanvas = MplCanvas(self, width=5.5, height=4, dpi=100)
        self.primaryCanvas.setFixedSize(640, 400)

        # Airfoil Parameter
        self.m = 0
        self.p = 0
        self.c = 0
        self.t = 0

        # Default airfoil (NACA 0012)
        self.airfoil = Naca4Digit(0, 0, 0.12, 1, 70)
        self.showFigure()

        # Status
        self.streamActive = False

        # Secondary Figure
        self.secondaryCanvas = MplCanvas(self, width=5.5, height=4, dpi=100)
        self.secondaryCanvas.setFixedSize(640, 400)

        #-----------------------------------------------------------------------
        # LAYOUTS
        #-----------------------------------------------------------------------
        # Main structure
        mainLayout = QHBoxLayout(self)
        leftMainLayout = QVBoxLayout()
        rightMainLayout = QVBoxLayout()

        # Title
        titleLayout = QVBoxLayout()
        titleLayout.setAlignment(Qt.AlignTop)

        # Main figure
        figureLayout = QHBoxLayout()
        figureLayout.setContentsMargins(30, 40, 30, 15)

        # Sliders
        sliderLayout = QVBoxLayout()

        # AoA slider
        alphaSliderLayout = QVBoxLayout()
        alphaSliderLayout.setContentsMargins(25, 15, 40, 15)

        # Velocity slider
        velocitySliderLayout = QVBoxLayout()
        velocitySliderLayout.setContentsMargins(25, 15, 40, 15)

        commandWindowLayout = QHBoxLayout()
        commandWindowLayout.setContentsMargins(20, 0, 25, 25)  # FIXME: No effect

        statisticsLayout = QVBoxLayout()
        statisticsLayout.setContentsMargins(20, 0, 25, 25)

        secondaryCanvasLayout = QHBoxLayout()
        secondaryCanvasLayout.setContentsMargins(20, 25, 40, 0)

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
        self.chordValues = [str(t) for t in chordValues]
        chordComboBox = QComboBox()
        chordComboBox.addItems(self.airfoilThicknessValues)
        chordComboBox.setFixedSize(70, 25)
        chordComboBox.setStyleSheet("color:white;")
        chordLabel = QLabel("Chord Length        ")
        chordLabel.setFont(QFont("serif", 10))
        chordLabel.setStyleSheet("color:white;")

        plotButton = QPushButton("Plot Airfoil")
        plotButton.setStyleSheet("color:White;")

        plotStreamButton = QPushButton("Plot Streamlines")
        plotStreamButton.setStyleSheet("color:White;")

        self.coefficientOfLiftLabel = QLabel("Sectional Lift Coefficient:  ")
        self.coefficientOfLiftLabel.setFont(QFont("mono", 10))
        self.coefficientOfLiftLabel.setStyleSheet("color:White;")



        self.commandWindow = QPlainTextEdit()
        self.commandWindow.setStyleSheet("background-color:rgb(60, 60, 60);")
        self.commandWindow.setFixedSize(640, 250)

        #-----------------------------------------------------------------------
        # LAYOUT MANAGEMENT
        #-----------------------------------------------------------------------
        titleLayout.addWidget(titleLabel)
        figureLayout.addWidget(self.primaryCanvas)

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
        airfoilOptionsLayout.addWidget(plotStreamButton)

        alphaSliderLayout.addWidget(alphaSlider)
        alphaSliderLayout.addWidget(self.alphaSliderLabel)
        velocitySliderLayout.addWidget(velocitySlider)
        velocitySliderLayout.addWidget(self.velocitySliderLabel)

        sliderLayout.addLayout(alphaSliderLayout)
        sliderLayout.addLayout(velocitySliderLayout)

        parametersLayout.addLayout(airfoilOptionsLayout)
        parametersLayout.addLayout(sliderLayout)

        statisticsLayout.addWidget(self.coefficientOfLiftLabel)

        secondaryCanvasLayout.addWidget(self.secondaryCanvas)
        # commandWindowLayout.addWidget(self.commandWindow)

        leftMainLayout.addLayout(figureLayout)
        leftMainLayout.addLayout(parametersLayout)
        # rightMainLayout.addWidget(self.secondaryCanvas)
        rightMainLayout.addLayout(secondaryCanvasLayout)
        # rightMainLayout.addLayout(commandWindowLayout)
        rightMainLayout.addLayout(statisticsLayout)
        # mainLayout.addLayout(figureLayout)
        # mainLayout.addLayout(parametersLayout)

        mainLayout.addLayout(leftMainLayout)
        mainLayout.addLayout(rightMainLayout)
        #-----------------------------------------------------------------------
        # SIGNAL MANAGEMENT
        #-----------------------------------------------------------------------
        alphaSlider.valueChanged.connect(self.alphaChanged)
        velocitySlider.valueChanged.connect(self.velocityChanged)
        plotButton.clicked.connect(self.setAirfoil)
        plotStreamButton.clicked.connect(self.plotStreamLines)

        camberComboBox.currentIndexChanged.connect(self.setCamber)
        camberLocationComboBox.currentIndexChanged.connect(self.setCamberLocation)
        airfoilThicknessComboBox.currentIndexChanged.connect(self.setThickness)
        chordComboBox.currentIndexChanged.connect(self.setChord)

    def alphaChanged(self, value):
        """ Update angle of attack """
        self.alphaSliderLabel.setText("Angle of Attack: {} deg".format(str(value)))
        self.airfoil.setAlpha(value*np.pi/180)
        if self.streamActive:
            self.plotStreamLines()

    def velocityChanged(self, value):
        """ Update free stream velocity """
        self.velocitySliderLabel.setText("Velocity: {} [m/s]".format(str(value)))
        self.airfoil.setVelocity(value)
        if self.streamActive:
            self.plotStreamLines()

    def setCamber(self, camberIndex):
        """ Update airfoil camber """
        self.m = int(float(self.camberValues[camberIndex]))/100

    def setCamberLocation(self, camberLocationIndex):
        """ Update airfoil maximum camber location """
        self.p = int(float(self.camberLocationValues[camberLocationIndex]))/10

    def setThickness(self, thicknessIndex):
        """ Update airfoil thickness """
        self.t = int(float(self.airfoilThicknessValues[thicknessIndex]))/100

    def setChord(self, chordIndex):
        """ Update airfoil chord length """
        self.c = int(float(self.chordValues[chordIndex]))

    def showFigure(self):
        """ Show the figure """
        self.primaryCanvas.axes.cla()
        self.airfoil.plotAirfoil(self.primaryCanvas)
        self.primaryCanvas.draw()

    def setAirfoil(self):
        """ Create airfoil """
        self.airfoil = Naca4Digit(self.m, self.p, self.t, self.c, 70)
        self.showAirfoil()

    def plotStreamLines(self):
        """ Plot airfoil stream function """
        self.airfoil.plotAirfoil(self.secondaryCanvas)
        coefficientOfLift = self.airfoil.plotStream(self.secondaryCanvas)
        self.secondaryCanvas.draw()
        self.streamActive = True

    def showAirfoil(self):
        self.airfoil.calculateAirfoilBorder(100)
        self.primaryCanvas.axes.cla()
        self.airfoil.plotAirfoil(self.primaryCanvas)
        self.primaryCanvas.draw()

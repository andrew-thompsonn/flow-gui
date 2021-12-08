from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox, QSlider, QPlainTextEdit
from PyQt5.QtGui import QFont

from PyQt5.QtCore import Qt
from numpy.lib.index_tricks import index_exp

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
        self.c = 1 
        self.t = 12 

        # Default airfoil (NACA 0012)
        self.airfoil = Naca4Digit(0, 0, 0.12, 1, 70)
        self.showFigure()

        self.N = 100 

        # Status
        self.streamActive = False

        # Secondary Figure
        self.secondaryCanvas = MplCanvas(self, width=5.5, height=4, dpi=100)
        self.secondaryCanvas.setFixedSize(750, 440)

        # Tertiary Figure
        self.tertiaryCanvas = MplCanvas(self, width=5.5, height=4, dpi=100)
        self.tertiaryCanvas.setFixedSize(640, 400)

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
        figureLayout.setContentsMargins(0, 25, 0, 15)

        # Sliders
        sliderLayout = QVBoxLayout()

        # AoA slider
        alphaSliderLayout = QVBoxLayout()
        alphaSliderLayout.setContentsMargins(25, 15, 40, 0)

        # Velocity slider
        velocitySliderLayout = QVBoxLayout()
        velocitySliderLayout.setContentsMargins(25, 0, 40, 0)

        statisticsLayout = QVBoxLayout()
        statisticsLayout.setContentsMargins(20, 0, 25, 85)

        secondaryCanvasLayout = QHBoxLayout()
        secondaryCanvasLayout.setContentsMargins(30, 25, 40, 0)

        tertiaryCanvasLayout = QHBoxLayout()
        tertiaryCanvasLayout.setContentsMargins(35, 0, 30, 0)

        airfoilOptionsLayout = QVBoxLayout()
        airfoilOptionsLayout.setContentsMargins(33, 15, 40, 100)

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
        camberComboBox.setStyleSheet("color:white; background-color:rgb(25, 25, 25)")
        camberLabel = QLabel("Camber                  ")
        camberLabel.setFont(QFont("serif", 10))
        camberLabel.setStyleSheet("color:white;")

        # Combo box for camber location & label
        camberLocationValues = np.linspace(0, 10, 11)
        self.camberLocationValues = [str(c) for c in camberLocationValues]
        camberLocationComboBox = QComboBox()
        camberLocationComboBox.addItems(self.camberLocationValues)
        camberLocationComboBox.setFixedSize(70, 25)
        camberLocationComboBox.setStyleSheet("color:white; background-color:rgb(25, 25, 25)")
        camberLocationLabel = QLabel("Camber Location        ")
        camberLocationLabel.setFont(QFont("serif", 10))
        camberLocationLabel.setStyleSheet("color:white;")

        # Combo box for airfoil thickness & label
        airfoilThicknessValues = np.linspace(0, 40, 41)
        self.airfoilThicknessValues = [str(t) for t in airfoilThicknessValues]
        airfoilThicknessComboBox = QComboBox()
        airfoilThicknessComboBox.addItems(self.airfoilThicknessValues)
        airfoilThicknessComboBox.setFixedSize(70, 25)
        airfoilThicknessComboBox.setStyleSheet("color:white; background-color:rgb(25, 25, 25)")
        airfoilThicknessLabel = QLabel("Airfoil Thickness      ")
        airfoilThicknessLabel.setFont(QFont("serif", 10))
        airfoilThicknessLabel.setStyleSheet("color:white;")

        chordValues = np.linspace(0, 40, 41)
        self.chordValues = [str(t) for t in chordValues]
        chordComboBox = QComboBox()
        chordComboBox.addItems(self.airfoilThicknessValues)
        chordComboBox.setFixedSize(70, 25)
        chordComboBox.setStyleSheet("color:white; background-color:rgb(25, 25, 25);")
        chordLabel = QLabel("Chord Length        ")
        chordLabel.setFont(QFont("serif", 10))
        chordLabel.setStyleSheet("color:white;")

        plotButton = QPushButton("Set Airfoil")
        plotButton.setStyleSheet("color:White; background-color:rgb(25, 25, 25);")

        clearButton = QPushButton("Clear")
        clearButton.setStyleSheet("color:White; background-color:rgb(25, 25, 25);")

        analyzeButton = QPushButton("Run Analysis")
        analyzeButton.setStyleSheet("color:White; background-color:rgb(25, 25, 25)")

        self.summaryLabel = QLabel(f"Summary: {self.airfoil.name}\n")
        self.summaryLabel.setFont(QFont("mono", 10))
        self.summaryLabel.setStyleSheet("color:white;")

        self.coefficientOfLiftLabel = QLabel("\tSectional Lift Coefficient:  ")
        self.coefficientOfLiftLabel.setFont(QFont("mono", 10))
        self.coefficientOfLiftLabel.setStyleSheet("color:White;")

        self.angleOfAttackLabel = QLabel("\tAngle of Attack:  ")
        self.angleOfAttackLabel.setFont(QFont("mono", 10))
        self.angleOfAttackLabel.setStyleSheet("color: white;")
        
        self.airVelocityLabel = QLabel("\tRelative Air Velocity:  ")
        self.airVelocityLabel.setFont(QFont("mono", 10))
        self.airVelocityLabel.setStyleSheet("color:White;")

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
        airfoilOptionsLayout.addWidget(analyzeButton)
        airfoilOptionsLayout.addWidget(clearButton)

        statisticsLayout.addWidget(self.summaryLabel) 
        statisticsLayout.addWidget(self.coefficientOfLiftLabel)
        statisticsLayout.addWidget(self.angleOfAttackLabel)
        statisticsLayout.addWidget(self.airVelocityLabel)

        alphaSliderLayout.addWidget(alphaSlider)
        alphaSliderLayout.addWidget(self.alphaSliderLabel)
        velocitySliderLayout.addWidget(velocitySlider)
        velocitySliderLayout.addWidget(self.velocitySliderLabel)

        sliderLayout.addLayout(alphaSliderLayout)
        sliderLayout.addLayout(velocitySliderLayout)
        sliderLayout.addLayout(statisticsLayout)

        parametersLayout.addLayout(airfoilOptionsLayout)
        parametersLayout.addLayout(sliderLayout)


        secondaryCanvasLayout.addWidget(self.secondaryCanvas)
        tertiaryCanvasLayout.addWidget(self.tertiaryCanvas)

        leftMainLayout.addLayout(secondaryCanvasLayout)
        leftMainLayout.addLayout(parametersLayout)
        rightMainLayout.addLayout(figureLayout)
        rightMainLayout.addLayout(tertiaryCanvasLayout)

        mainLayout.addLayout(leftMainLayout)
        mainLayout.addLayout(rightMainLayout)
        #-----------------------------------------------------------------------
        # SIGNAL MANAGEMENT
        #-----------------------------------------------------------------------
        alphaSlider.valueChanged.connect(self.alphaChanged)
        velocitySlider.valueChanged.connect(self.velocityChanged)
        plotButton.clicked.connect(self.setAirfoil)
        analyzeButton.clicked.connect(self.plotStreamLines)
        # analyzeButton.clicked.connect(self.performFullAnalysis)

        camberComboBox.currentIndexChanged.connect(self.setCamber)
        camberLocationComboBox.currentIndexChanged.connect(self.setCamberLocation)
        airfoilThicknessComboBox.currentIndexChanged.connect(self.setThickness)
        chordComboBox.currentIndexChanged.connect(self.setChord)
        clearButton.clicked.connect(self.clearFigures)

        self.clearFigures()

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
        self.airfoil = Naca4Digit(self.m, self.p, self.t, self.c, self.N)
        self.showAirfoil()

    def plotStreamLines(self):
        """ Plot airfoil stream function """
        self.clearFigures() 
        self.airfoil.plotWashedAirfoil(self.secondaryCanvas)
        coefficientOfLift, cp = self.airfoil.plotStream(self.secondaryCanvas, pressurePlot=True)
        coefficientOfLift = round(coefficientOfLift[0], 3)

        l = len(self.airfoil.xPts)
        self.tertiaryCanvas.axes.plot(self.airfoil.xPts[:l//2], cp[:l//2], 'b', marker='o', linewidth=3.5, label="Lower Surface")
        self.tertiaryCanvas.axes.plot(self.airfoil.xPts[l//2:-1], cp[l//2:], 'r', marker='o', linewidth=3.5, label="Upper Surface")
        self.tertiaryCanvas.axes.legend()
        self.tertiaryCanvas.axes.set_xlim((0, self.airfoil.chord))
        self.tertiaryCanvas.axes.set_ylim((np.min(cp), np.max(cp)))
        self.tertiaryCanvas.axes.invert_yaxis()
        self.tertiaryCanvas.draw()

        self.summaryLabel.setText(f"Summary: {self.airfoil.name}\n")
        self.coefficientOfLiftLabel.setText(f"\tSectional Lift Coefficient:\t\t{coefficientOfLift}")
        self.angleOfAttackLabel.setText(f"\tAngle of Attack:\t\t\t{round(self.airfoil.alpha*180/np.pi)} [deg]")
        self.airVelocityLabel.setText(f"\tRelative Air Velocity:\t\t{self.airfoil.vInf} [m/s]")


        self.secondaryCanvas.draw()
        self.streamActive = True

    def showAirfoil(self):
        """ Plot the shape of the airfoil """
        self.airfoil.calculateAirfoilBorder(self.N)
        self.airfoil.plotAirfoil(self.primaryCanvas)
        self.primaryCanvas.draw()

    def altitudeChanged(self, value):
        """ Change the altitude used in the std atm model """
        self.altitudeSliderLabel.setText(f"Altitude: {value} [m]")

    def clearFigures(self):
        self.primaryCanvas.axes.clear()
        self.secondaryCanvas.axes.clear()
        self.tertiaryCanvas.axes.clear()

        self.tertiaryCanvas.axes.set_title("Coefficient of Pressure vs Fractional Chord Length", color='white')
        self.tertiaryCanvas.axes.set_ylabel("Cp")
        self.tertiaryCanvas.axes.set_xlabel("x/c")
        self.tertiaryCanvas.axes.xaxis.label.set_color('white')
        self.tertiaryCanvas.axes.yaxis.label.set_color('white')
        self.tertiaryCanvas.axes.tick_params(axis='x', colors='grey')
        self.tertiaryCanvas.axes.tick_params(axis='y', colors='grey')
        self.tertiaryCanvas.axes.grid(True, color='gray', linestyle='-.')
        self.tertiaryCanvas.axes.plot(np.linspace(-5, 10, 25), np.zeros(25,), 'white')
        self.tertiaryCanvas.axes.set_xlim((-0.01*self.c, self.c*1.1))
        
        self.secondaryCanvas.axes.set_title("Stream Function", color='white')
        self.secondaryCanvas.axes.set_xlabel("X [m]")
        self.secondaryCanvas.axes.set_ylabel("Y [m]")
        self.secondaryCanvas.axes.xaxis.label.set_color('white')
        self.secondaryCanvas.axes.yaxis.label.set_color('white')
        self.secondaryCanvas.axes.set_xlim((-2*self.airfoil.chord, 2*self.airfoil.chord))
        self.secondaryCanvas.axes.tick_params(axis='x', colors='grey')
        self.secondaryCanvas.axes.tick_params(axis='y', colors='grey')
        # self.secondaryCanvas.axes.grid(True, color='gray', linestyle='-.')

        self.airfoil.plotAirfoil(self.primaryCanvas)
        self.primaryCanvas.draw()
        self.secondaryCanvas.draw()
        self.tertiaryCanvas.draw()
#!/usr/bin/env python

from PyQt5.QtWidgets import QApplication
from GUI.main_window import MainWindow

import sys

def main():
    """ A NACA airfoil plotting and analyisis tool. Possible functionalities:

        CORE FEATURES --

        1. Plot a given NACA 4 digit airfoil.

        2. Pull wind tunnel data from web. Using an API if possible.

        3. Apply thin airfoil theory and/or vortex panel to plot the
           streamlines, equipotential lines, and pressure contours at given
           AoA and flow parameters.

        4. Options to overlay pressure, flow, and stream lines, add sliders to
           change flow parameters with live updates to current figure

        STRETCH FEATURES --

        5. (Possibly) Compare analysis of multiple airfoils side by side.

        6. Add in estimates for three dimensional aircraft, possibly provide
           values for obscure coefficients such as oswald's efficiency factor.
    """
    # Create application
    app = QApplication(sys.argv)
    # Create Main window
    mainWindow = MainWindow()
    # Show the main window
    mainWindow.show()
    # Run the application
    exit(app.exec())

if __name__ == "__main__":
    main()

#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np
from CFD.NACA_4_Digit import Naca4Digit


def computeRadius(xCenter, yCenter, x, y):
    r = np.sqrt((x - xCenter) ** 2 + (y - yCenter) ** 2)
    return r


def main():
    alpha = 8*np.pi/180
    velocity = 20

    airfoil = Naca4Digit(0, 0, 0.12, 2, 500)
    # airfoil = Naca4Digit(1, 4, 0.08, 1, 100)
    xb, yb = airfoil.calculateAirfoilBorder(40)
    xPts, yPts, circulations = airfoil.vortexPanel(xb, yb, velocity, alpha)

    x, y = np.meshgrid(np.linspace(-1, 3, 100), np.linspace(-1, 3, 100))
    airfoilStream = np.zeros(np.shape(x))

    for index in range(len(circulations)):
        radius = computeRadius(xPts[index], yPts[index], x, y)
        # theta = np.atan2(y - yPts[index], x - xPts[index])

        # FIXME: Removed a negative from this equation...
        vortexStream = (circulations[index]/(2*np.pi))*np.log(radius)
        airfoilStream = airfoilStream + vortexStream

    freeStream = y*velocity*np.cos(alpha) - x*velocity*np.sin(alpha)
    airfoilStream = airfoilStream + freeStream
    """
            For each panel, compute the velocity as a function of x,y
                            compute the stream as a function of x,y
                            compute the potential as a function of x,y
                            sum the velocity, stream, and potential functions at each point 
                            
            Add the free stream velocity, stream, and potential functions to the sum
            
            psi = (-Tau/(2*pi)) * ln(r)
            phi = (Tau/(2*pi))  * theta
            vTheta = Tau/(2*pi*radius)
            
    """


    plt.figure()

    plt.xlabel('x', fontsize=16)
    plt.ylabel('y', fontsize=16)
    plt.axis('equal')

    plt.contour(x, y, airfoilStream, 100)
    plt.plot(airfoil.xPts, airfoil.yPts, 'r', linewidth=2)
    plt.show()


if __name__ == "__main__":
    main()

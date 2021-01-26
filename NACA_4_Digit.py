#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np

from mpl_canvas import MplCanvas

class Naca4Digit():

    """ A class to represent a NACA 4-digit airfoil """
    def __init__(self, m, p, t, c, N):
        # Maximum camber
        self.maxCamber = m
        # Location of maximum camber
        self.camberPt = p
        # Maximum thickness
        self.thickness = t
        # Chord length
        self.chord = c
        # Name
        self.name = "NACA "+str(int(m*100))+str(int(p*10))+str(int(t*100))
        # Am I a fucking dipshit?
        self.andrewIsStupid = True

    def calculateAirfoilBorder(self):
        """ Calculates airfoil x and y values """
        # Unpack values
        c = self.chord
        p = self.camberPt
        t = self.thickness
        m = self.maxCamber

        # Airfoil Thickness & X boundary panel points
        x = np.linspace(0, c, 100)
        yt = (t/0.2)*c*(.2969*(x/c)**.5-0.1260*(x/c)-.3516*(x/c)**2+ \
             .2843*(x/c)**3-0.1036*(x/c)**4)

        # If airfoil is symmetric
        if m == 0 and p == 0:
            # Upper/lower surfaces
            ytUpper = list(yt)
            ytLower = list(-yt)
            xUpper = list(x)
            xLower = list(np.linspace(c, 0, 100))

            # Formatting
            ytLower.reverse()
            x = xUpper + xLower
            y = ytUpper + ytLower

        # If airfoil is non symmetric
        else:
            # yc equations
            yc1 = lambda x: m*x/(p**2)*(2*p-(x/c))
            yc2 = lambda x: m*(c-x)/(1-p)**2*(1+(x/c)-2*p)
            yc1Values = [yc1(xpt) for xpt in x if xpt < p*c]
            yc2Values = [yc2(xpt) for xpt in x if xpt >= p*c]
            yc = yc1Values + yc2Values

            # dyc/dx equations
            dyc1 = lambda x: -2*m*(2*p-(x/c))/(c*p**2)
            dyc2 = lambda x: -2*m*(x-c*p)/(c*(p-1)**2)
            dyc1Values = [dyc1(xpt) for xpt in x if xpt < p*c]
            dyc2Values = [dyc2(xpt) for xpt in x if xpt >= p*c]
            dycDx = dyc1Values + dyc2Values

            # Calculate xi values
            xi = [np.arctan(dyc) for dyc in dycDx]

            # Calculate boundary points
            xUpper = list(x - yt*np.sin(xi))
            xLower = list(x + yt*np.sin(xi))
            yUpper = list(yc + yt*np.cos(xi))
            yLower = list(yc - yt*np.cos(xi))

            # Formatting
            xLower.reverse()
            yLower.reverse()
            x = xUpper + xLower
            y = yUpper + yLower

        return x, y

    def generateContours(self, alpha, rho, v):
        """ Generate data for stream, potential, and pressure contours """
        return None

    def vortexPanel(self):
        """ Employ vortex panel method to calculate lift """
        return None

    def plotAirfoil(self, x, y, canvas):
        """ Plot an airfoil """
        canvas.axes.set_xlim((-10*self.chord, 2*self.chord))
        # Plot the airfoil
        canvas.axes.plot(x, y, 'b')
        # Plot the airfoil
        canvas.axes.plot(x, y, linewidth = 2)
        # Show a grid
        canvas.axes.grid(True, color = 'gray', linestyle = '-.')
        # Keep axes equal
        canvas.axes.axis('equal')
        # Set title as airfoil name
        canvas.axes.set_title(self.name, color = 'white')
        # Set x axis label
        canvas.axes.set_xlabel("X [m]")
        # Set y axis label
        canvas.axes.set_ylabel("Y [m]")
        # Set color of axis labels
        canvas.axes.xaxis.label.set_color('white')
        canvas.axes.yaxis.label.set_color('white')
        # Set color of axes ticks
        canvas.axes.tick_params(axis='x', colors='grey')
        canvas.axes.tick_params(axis='y', colors='grey')
        # Return the canvas object
        return canvas

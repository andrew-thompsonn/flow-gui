#!/usr/bin/env python

import numpy as np
import math


class Stream:
    """ A class to represent the free stream conditions of flight """
    def __init__(self, velocity, density, alpha, resolution, xRange, yRange):
        self.velocity = velocity
        self.density = density
        self.alpha = alpha
        self.resolution = resolution
        self.xRange = xRange
        self.yRange = yRange

    def computeStreamLines(self):
        """ Compute the free stream potential and stream functions """
        xAxis = np.linspace(self.xRange[0], self.xRange[1], self.resolution)
        yAxis = np.linspace(self.yRange[0], self.xRange[1], self.resolution)
        x, y = np.meshgrid(xAxis, yAxis)
        freeStream = y*self.velocity*math.cos(self.alpha) - x*self.velocity*math.sin(self.alpha)
        freePotential = x*self.velocity*math.cos(self.alpha) + y*self.velocity*math.sin(self.alpha)
        return freeStream, freePotential

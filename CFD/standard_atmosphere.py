import numpy as np

class StandardAtmosphere:
    def __init__(self):
        self.earthRadius = 6371
        self.hydroStaticConstant = 34.163

    def getDensity(self, altitude):
        geopotentialAltitude = altitude*self.earthRadius/(altitude + self.earthRadius)

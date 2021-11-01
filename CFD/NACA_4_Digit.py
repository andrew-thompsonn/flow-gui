import numpy as np
import math

""" Homegrown vortex panel implementation & visualization """

class Naca4Digit:
    """ A class to represent a NACA 4-digit airfoil """
    def __init__(self, m, p, t, c, N):
        self.maxCamber = m  # maximum camber
        self.camberLocation = p  # maximum camber location
        self.thickness = t  # maximum thickness
        self.chord = c  # chord length

        self.name = "NACA " + str(int(m * 100)) + str(int(p * 10)) + str(int(t * 100))
        self.vInf = 0
        self.alpha = 0
        self.xPts = None
        self.yPts = None
        self.calculateAirfoilBorder(N)

        self.gx, self.gy = np.meshgrid(np.linspace(-3*self.chord, 2*self.chord, 100),
                                       np.linspace(-1.5*self.chord, 1.5*self.chord, 100))

    def computeThickness(self, xLocation):
        """ Compute the airfoil thickness at a location on the x axis """
        thickness = (self.thickness / 0.2) * self.chord * (
                    0.2969 * (xLocation / self.chord) ** .5 - 0.1260 * (xLocation / self.chord)
                    - 0.3516 * (xLocation / self.chord) ** 2 + 0.2843 * (xLocation / self.chord) ** 3
                    - 0.1036 * (xLocation / self.chord) ** 4)
        return thickness

    def computeCamber(self, xLocation):
        """ Compute the airfoil camber at a location on the x axis """
        if xLocation < self.camberLocation * self.chord:
            camber = self.maxCamber * (xLocation / self.camberLocation ** 2) * (
                        2 * self.camberLocation - (xLocation / self.chord))
        else:
            camber = self.maxCamber * ((self.chord - xLocation) / (1 - self.camberLocation) ** 2) * (
                        1 + (xLocation / self.chord) - 2 * self.camberLocation)
        return camber

    def calculateAirfoilBorder(self, N):
        """ Calculates airfoil x and y values """
        c = self.chord
        p = self.camberLocation
        t = self.thickness
        m = self.maxCamber

        dydxFunc = lambda x1, yc1, x, yc: (yc1 - yc) / (x1 - x)
        zetaFunc = lambda dydx: math.atan(dydx)

        x = np.zeros((N, 1))
        y = np.zeros((N, 1))
        stepSize = c / N
        xStepBottom = np.linspace(c, 0, math.floor(N / 2))
        xStepTop = np.linspace(stepSize, c, math.ceil(N / 2))
        xSteps = np.concatenate((xStepBottom, xStepTop))
        index = 0

        for xStep in xSteps:
            if m == 0 and p == 0:
                x[index] = xStep
                if index < math.floor(N / 2):
                    y[index] = -self.computeThickness(xStep)
                else:
                    y[index] = self.computeThickness(xStep)
            else:
                yt = self.computeThickness(xStep)
                yc1 = self.computeCamber(xStep)
                yc = self.computeCamber(xStep + stepSize)
                dydx = dydxFunc(xStep + stepSize, yc1, xStep, yc)
                zeta = zetaFunc(dydx)
                if index <= math.floor(N / 2):
                    x[index] = xStep + yt * math.sin(zeta)
                    y[index] = yc1 - yt * math.cos(zeta)
                else:
                    x[index] = xStep - yt * math.sin(zeta)
                    y[index] = yc1 + yt * math.cos(zeta)
            index += 1
        self.xPts = x
        self.yPts = y
        return x, y

    def setVelocity(self, vInfIn):
        """ Set the velocity parameter """
        self.vInf = vInfIn

    def setAlpha(self, alphaIn):
        """ Set the angle of attack parameter """
        self.alpha = alphaIn

    @staticmethod
    def vortexPanel(xb, yb, vInf, alpha):
        """ Employ vortex panel method to calculate lift, pressure, circulation etc. """
        m = len(xb) - 1
        mp1 = m + 1
        x = np.zeros((m, 1))
        y = np.zeros((m, 1))
        s = np.zeros((m, 1))
        sine = np.zeros((m, 1))
        cosine = np.zeros((m, 1))
        theta = np.zeros((m, 1))
        RHS = np.zeros((mp1, 1))
        cn1 = np.zeros((m, m))
        cn2 = np.zeros((m, m))
        ct1 = np.zeros((m, m))
        ct2 = np.zeros((m, m))
        an = np.zeros((mp1, mp1))
        at = np.zeros((m, mp1))

        for index in range(m):
            indexP1 = index + 1
            x[index] = 0.5 * (xb[index] + xb[indexP1])
            y[index] = 0.5 * (yb[index] + yb[indexP1])

            s[index] = np.sqrt((xb[indexP1] - xb[index]) ** 2 + (yb[indexP1] - yb[index]) ** 2)
            theta[index] = np.arctan2(yb[indexP1] - yb[index], xb[indexP1] - xb[index])
            sine[index] = math.sin(theta[index])
            cosine[index] = math.cos(theta[index])
            RHS[index] = math.sin(theta[index] - alpha)

        for idx1 in range(m):
            for idx2 in range(m):

                if idx1 == idx2:
                    cn1[idx1, idx2] = -1
                    cn2[idx1, idx2] = 1
                    ct1[idx1, idx2] = 0.5 * math.pi
                    ct2[idx1, idx2] = 0.5 * math.pi
                else:
                    A = -(x[idx1] - xb[idx2]) * cosine[idx2] - (y[idx1] - yb[idx2]) * sine[idx2]
                    B = (x[idx1] - xb[idx2]) ** 2 + (y[idx1] - yb[idx2]) ** 2
                    C = math.sin(theta[idx1] - theta[idx2])
                    D = math.cos(theta[idx1] - theta[idx2])
                    E = (x[idx1] - xb[idx2]) * sine[idx2] - (y[idx1] - yb[idx2]) * cosine[idx2]
                    F = math.log(1 + s[idx2] * (s[idx2] + 2 * A) / B)
                    G = math.atan2(E * s[idx2], B + A * s[idx2])
                    P = (x[idx1] - xb[idx2]) * math.sin(theta[idx1] - 2 * theta[idx2]) + (
                            y[idx1] - yb[idx2]) * math.cos(theta[idx1] - 2 * theta[idx2])
                    Q = (x[idx1] - xb[idx2]) * math.cos(theta[idx1] - 2 * theta[idx2]) - (
                            y[idx1] - yb[idx2]) * math.sin(theta[idx1] - 2 * theta[idx2])

                    cn2[idx1, idx2] = D + 0.5 * Q * F / s[idx2] - (A * C + D * E) * G / s[idx2]
                    cn1[idx1, idx2] = 0.5 * D * F + C * G - cn2[idx1, idx2]
                    ct2[idx1, idx2] = C + 0.5 * P * F / s[idx2] + (A * D - C * E) * G / s[idx2]
                    ct1[idx1, idx2] = 0.5 * C * F - D * G - ct2[idx1, idx2]

        for row in range(m):
            an[row, 0] = cn1[row, 0]
            an[row, m] = cn2[row, m - 1]
            at[row, 0] = ct1[row, 0]
            at[row, m] = ct2[row, m - 1]

            for col in range(1, m):
                an[row, col] = cn1[row, col] + cn2[row, col - 1]
                at[row, col] = ct1[row, col] + ct2[row, col - 1]

        an[m, 0] = 1
        an[m, m] = 1
        for col in range(1, m):
            an[m, col] = 0
        RHS[m] = 0

        gamma = np.linalg.solve(an, RHS)
        velocityAngle = theta - alpha
        velocity = np.cos(velocityAngle) + np.matmul(at, gamma)
        chord = max(xb) - min(xb)

        circulation = vInf*np.multiply(velocity, s)
        pressureCoefficient = 1 - np.multiply(velocity, velocity)
        liftCoefficient = np.sum(2*circulation)/(vInf*chord)
        return x, y, circulation, liftCoefficient

    @staticmethod
    def computeRadius(xCenter, yCenter, x, y):
        """ Compute the radii across the grid for a given (x, y) coordinate """
        return np.sqrt((x - xCenter) ** 2 + (y - yCenter) ** 2)

    def computeStreamlines(self):
        """ Compute the stream function for the given airfoil/flow """
        xPts, yPts, circulations, cl = self.vortexPanel(self.xPts, self.yPts, self.vInf, self.alpha)
        airfoilStream = np.zeros(np.shape(self.gx))

        for index in range(len(circulations)):
            radius = self.computeRadius(xPts[index], yPts[index], self.gx, self.gy)
            # theta = np.atan2(y - yPts[index], x - xPts[index])
            # FIXME: Removed a negative from this equation...
            vortexStream = (circulations[index]/(2*np.pi))*np.log(radius)
            airfoilStream = airfoilStream + vortexStream

        freeStream = self.gy*self.vInf*np.cos(self.alpha) - self.gx*self.vInf*np.sin(self.alpha)
        return airfoilStream + freeStream, cl

    def plotStream(self, canvas):
        """ Plot the stream lines for the airfoil and flow """
        airfoilStream, cl = self.computeStreamlines()
        canvas.axes.contour(self.gx, self.gy, airfoilStream, 40)
        return cl

    def plotAirfoil(self, canvas):
        """ Plot an airfoil """
        camberLine = [self.computeCamber(xStep) for xStep in np.linspace(0, self.chord, 40)]
        canvas.axes.clear()
        canvas.axes.set_xlim((-10 * self.chord, 2 * self.chord))
        canvas.axes.fill(self.xPts, self.yPts, color='gray')
        canvas.axes.plot(self.xPts, self.yPts, linewidth=2.5)
        canvas.axes.plot(np.linspace(0, self.chord, 40), camberLine, color='red')
        canvas.axes.grid(True, color='gray', linestyle='-.')
        canvas.axes.axis('equal')
        canvas.axes.set_title(self.name, color='white')
        canvas.axes.set_xlabel(" ")
        canvas.axes.set_ylabel(" ")
        canvas.axes.xaxis.label.set_color('white')
        canvas.axes.yaxis.label.set_color('white')
        canvas.axes.tick_params(axis='x', colors='grey')
        canvas.axes.tick_params(axis='y', colors='grey')
        return canvas


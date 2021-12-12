#!/usr/bin/env python

from numpy.lib.function_base import angle
from NACA_4_Digit import Naca4Digit
import matplotlib.pyplot as plt
import numpy as np

VELOCITY = 55
POINTS = 100

def main():
    naca0012 = Naca4Digit(0.0,  0.0,  0.12, 1, POINTS)
    naca2412 = Naca4Digit(0.02, 0.40, 0.12, 1, POINTS)
    naca4412 = Naca4Digit(0.04, 0.40, 0.12, 1, POINTS)

    naca0012.setVelocity(VELOCITY)
    naca2412.setVelocity(VELOCITY)
    naca4412.setVelocity(VELOCITY)

    cL0012, cL2412, cL4412 = [], [], []
    anglesOfAttack = list(range(-4, 10)) 

    print("Beginning analysis")

    for angleOfAttack in anglesOfAttack:

        print(f"Running model for {angleOfAttack} degree AoA...")

        naca0012.setAlpha(angleOfAttack*np.pi/180)
        naca2412.setAlpha(angleOfAttack*np.pi/180)
        naca4412.setAlpha(angleOfAttack*np.pi/180)

        freeStream, cl0012, pressure, cp = naca0012.computeStreamlines()
        freeStream, cl2412, pressure, cp = naca2412.computeStreamlines()
        freeStream, cl4412, pressure, cp = naca4412.computeStreamlines()

        cL0012.append(cl0012[0])
        cL2412.append(cl2412[0])
        cL4412.append(cl4412[0])

        print(cl0012, cl2412, cl4412)

    print("\nModeling complete. Generating figure...")

    plt.figure()
    plt.title("Coefficient of Lift vs Angle of Attack")
    plt.plot(anglesOfAttack, cL0012, label='NACA 0012')
    plt.plot(anglesOfAttack, cL2412, label='NACA 2412')
    plt.plot(anglesOfAttack, cL4412, label='NACA 4412')
    plt.legend(); plt.grid()
    plt.xlabel("Angle of Attack [deg]")
    plt.ylabel("Coefficient of Lift")
    plt.savefig("lift_curve.jpg")

    print("Complete. Figure saved as \'lift_curve.jpg\'")


if __name__ == "__main__":
    main()
#!/usr/bin/env python

import math
import numpy
from matplotlib import pyplot


def get_velocity_doublet(strength, xd, yd, X, Y):

    u = (-strength / (2 * math.pi) *
         ((X - xd)**2 - (Y - yd)**2) /
         ((X - xd)**2 + (Y - yd)**2)**2)
    v = (-strength / (2 * math.pi) *
         2 * (X - xd) * (Y - yd) /
         ((X - xd)**2 + (Y - yd)**2)**2)

    return u, v


def get_stream_function_doublet(strength, xd, yd, X, Y):

    psi = -strength / (2 * math.pi) * (Y - yd) / ((X - xd)**2 + (Y - yd)**2)

    return psi


def main():
    N = 50
    x_start, x_end = -2.0, 2.0
    y_start, y_end = -1.0, 1.0
    x = numpy.linspace(x_start, x_end, N)
    y = numpy.linspace(y_start, y_end, N)
    X, Y = numpy.meshgrid(x, y)

    kappa = 1.0                           # strength of the doublet
    x_doublet, y_doublet = 0.0, 0.0       # location of the doublet

    u_inf = 1.0

    # compute the velocity field on the mesh grid
    u_doublet, v_doublet = get_velocity_doublet(kappa, x_doublet, y_doublet, X, Y)

    # compute the stream-function on the mesh grid
    psi_doublet = get_stream_function_doublet(kappa, x_doublet, y_doublet, X, Y)

    # freestream velocity components
    u_freestream = u_inf * numpy.ones((N, N), dtype=float)
    v_freestream = numpy.zeros((N, N), dtype=float)

    # stream-function of the freestream flow
    psi_freestream = u_inf * Y

    # superposition of the doublet on the freestream flow
    u = u_freestream + u_doublet
    v = v_freestream + v_doublet
    psi = psi_freestream + psi_doublet

    # plot the streamlines
    width = 10
    height = (y_end - y_start) / (x_end - x_start) * width
    pyplot.figure(figsize=(width, height))
    pyplot.xlabel('x', fontsize=16)
    pyplot.ylabel('y', fontsize=16)
    pyplot.xlim(x_start, x_end)
    pyplot.ylim(y_start, y_end)
    pyplot.streamplot(X, Y, u, v, density=2, linewidth=1, arrowsize=1, arrowstyle='->')
    pyplot.scatter(x_doublet, y_doublet, color='#CD2305', s=80, marker='o')

    # calculate the cylinder radius and add the cylinder to the figure
    R = math.sqrt(kappa / (2 * math.pi * u_inf))
    circle = pyplot.Circle((0, 0), radius=R, color='#CD2305', alpha=0.5)
    pyplot.gca().add_patch(circle)

    # calculate the stagnation points and add them to the figure
    x_stagn1, y_stagn1 = +math.sqrt(kappa / (2 * math.pi * u_inf)), 0.0
    x_stagn2, y_stagn2 = -math.sqrt(kappa / (2 * math.pi * u_inf)), 0.0
    pyplot.scatter([x_stagn1, x_stagn2], [y_stagn1, y_stagn2],
                   color='g', s=80, marker='o');

    pyplot.show()


if __name__ == "__main__":
    main()

#!/usr/bin/env python

import matlab.engine


def main():
    """ Test being able to run Matlab script from .py file """
    eng = matlab.engine.start_matlab()




if __name__ == "__main__":
    main()

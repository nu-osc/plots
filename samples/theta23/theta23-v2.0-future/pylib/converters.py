#!/usr/bin/env python

import numpy as np

unity = lambda val: val

def amplitude_single_double(single2):
    return 4.0*single2*(1.0-single2)

def degrees_to_single(deg):
    return np.sin(np.radians(deg))**2
    
def amplitude_double_single(double2):
    return (1 - np.sqrt(1-double2))/2.0

converters = dict(
        amplitude13=dict(single=amplitude_single_double, double=unity),
        amplitude23=dict(single=unity, double=amplitude_double_single, degrees=degrees_to_single)
        )

def convert(var, mode, *vals):
    try:
        fcn = converters[var][mode]
    except KeyError:
        raise Exception(f'Do not know how to convert {var} {type}')

    return map(fcn, vals)


#!/usr/bin/env python

unity = lambda val: val

def amplitude_single_double(single2):
    return 4.0*single2*(1.0-single2)

converters = dict(
        amplitude13=dict(single=amplitude_single_double, double=unity),
        amplitude23=dict(single=amplitude_single_double, double=unity)
        )

def convert(var, mode, *vals):
    try:
        fcn = converters[var][mode]
    except KeyError:
        raise Exception(f'Do not know how to convert {var} {type}')

    return map(fcn, vals)


#!/usr/bin/env python

import numpy as np

unity = lambda val, **kwargs: val

def amplitude_single_double(single2, **kwrgs):
    return 4.0*single2*(1.0-single2)

def splitting_large_ee(dmee, context):
    ordering = context['ordering']=='NO' and 1.0 or -1.0
    dmSq21 = context['dmSq21']*1.e3 # dm32 is multiplied by 1.e3
    sinSqTheta12 = context['sinSqTheta12']
    cosSqTheta12 = 1.0 - sinSqTheta12
    dm32 = dmee - ordering * cosSqTheta12 * dmSq21
    return dm32

def radians_to_pi(rad, **kwargs):
    return rad/np.pi

def degrees_to_pi(deg, **kwargs):
    return np.radians(deg)/np.pi

converters = dict(
        amplitude13=dict(single=amplitude_single_double, double=unity),
        amplitude23=dict(single=amplitude_single_double, double=unity),
        splitting_large={'32': unity, 'ee': splitting_large_ee},
        deltaCP = dict(pi=unity, radians=radians_to_pi, degrees=degrees_to_pi)
        )

def convert(var, mode, *vals, **kwargs):
    try:
        fcn = converters[var][mode]
    except KeyError:
        raise Exception(f'Do not know how to convert {var} {mode}')

    def converter(val):
        return fcn(val, **kwargs)

    return map(converter, vals)


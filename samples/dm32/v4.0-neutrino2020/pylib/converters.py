#!/usr/bin/env python

unity = lambda val, **kwargs: val

def amplitude_single_double(single2, **kwrgs):
    return 4.0*single2*(1.0-single2)

def splitting_large_ee(dmee, **kwargs):
    return dmee

converters = dict(
        amplitude13=dict(single=amplitude_single_double, double=unity),
        amplitude23=dict(single=amplitude_single_double, double=unity),
        splitting_large={'32': unity, 'ee': splitting_large_ee}
        )

def convert(var, mode, *vals, **kwargs):
    try:
        fcn = converters[var][mode]
    except KeyError:
        raise Exception(f'Do not know how to convert {var} {mode}')

    def converter(val):
        return fcn(val, **kwargs)

    return map(converter, vals)


#!/usr/bin/env python

unity = lambda val, **kwargs: val

def amplitude_single_double(single2, **kwrgs):
    """
    sin²2θ = 4 sin²θ (1 - sin²θ)
    """
    return 4.0*single2*(1.0-single2)

def dm32_from_ee(dmee, context):
    """
    |Δm²₃₂| = |Δm²(ee)| - α cos²θ₁₂ Δm²₂₁
    """
    ordering = context['ordering']=='NO' and 1.0 or -1.0
    dmSq21 = context['dmSq21']*1.e3 # dm32 is multiplied by 1.e3
    sinSqTheta12 = context['sinSqTheta12']
    cosSqTheta12 = 1.0 - sinSqTheta12
    dm32 = dmee - ordering * cosSqTheta12 * dmSq21
    return dm32

def dm31_from_ee(dmee, context):
    """
    |Δm²₃₁| = |Δm²(ee)| + α sin²θ₁₂ Δm²₂₁
    """
    ordering = context['ordering']=='NO' and 1.0 or -1.0
    dmSq21 = context['dmSq21']*1.e3 # dm32 is multiplied by 1.e3
    sinSqTheta12 = context['sinSqTheta12']
    dm32 = dmee + ordering * sinSqTheta12 * dmSq21
    return dm32

def dm32_from_avg(dmavg, context):
    """
    |Δm²₃₂| = |Δm²(avg)| - α Δm²₂₁ / 2
    """
    ordering = context['ordering']=='NO' and 1.0 or -1.0
    dmSq21 = context['dmSq21']*1.e3 # dm32 is multiplied by 1.e3
    dm32 = dmavg - 0.5 * ordering * dmSq21
    return dm32

def dm31_from_avg(dmavg, context):
    """
    |Δm²₃₁| = |Δm²(avg)| + α Δm²₂₁ / 2
    """
    ordering = context['ordering']=='NO' and 1.0 or -1.0
    dmSq21 = context['dmSq21']*1.e3 # dm32 is multiplied by 1.e3
    dm32 = dmavg + 0.5 * ordering * dmSq21
    return dm32

def dm32_from_31(dm31, context):
    """
    |Δm²₃₂| = |Δm²₃₁| - α Δm²₂₁
    """
    ordering = context['ordering']=='NO' and 1.0 or -1.0
    dmSq21 = context['dmSq21']*1.e3 # dm32 is multiplied by 1.e3
    dm32 = dm31 - ordering * dmSq21
    return dm32

def dm32_from_32NO(dm32NO, context):
    """
    assume Δm²(ee) [NO]=Δm²(ee) [IO]
    input: |Δm²|
    |Δm²₃₂| = |Δm²|                   (NO)
    |Δm²₃₂| = |Δm²| + 2 cos²θ₁₂ Δm²₂₁ (IO)
    """
    ordering = context['ordering']=='NO' and 1.0 or -1.0
    if ordering==1.0:
        return dm32NO

    dmSq21 = context['dmSq21']*1.e3 # dm32 is multiplied by 1.e3
    sinSqTheta12 = context['sinSqTheta12']
    cosSqTheta12 = 1.0 - sinSqTheta12
    dm32IO = dm32NO + 2.0 * cosSqTheta12 * dmSq21
    return dm32IO

def dm32_from_32NO_31IO(dm32NO_31IO, context):
    """
    input: |Δm²|
    |Δm²₃₂| = |Δm²|         (NO)
    |Δm²₃₂| = |Δm²| + Δm²₂₁ (IO)
    """
    ordering = context['ordering']=='NO' and 1.0 or -1.0
    if ordering==1.0:
        return dm32NO_31IO

    return dm32_from_31(dm32NO_31IO, context)

def dm31_from_32NO_31IO(dm32NO_31IO, context):
    """
    input: |Δm²|
    |Δm²₃₁| = |Δm²| + Δm²₂₁ (NO)
    |Δm²₃₁| = |Δm²|         (IO)
    """
    ordering = context['ordering']=='NO' and 1.0 or -1.0
    if ordering==-1.0:
        return dm32NO_31IO

    return dm31_from_32(dm32NO_31IO, context)

def dm31_from_32(dm32, context):
    """
    |Δm²₃₁| = |Δm²₃₂| + α Δm²₂₁
    """
    ordering = context['ordering']=='NO' and 1.0 or -1.0
    dmSq21 = context['dmSq21']*1.e3 # dm32 is multiplied by 1.e3
    dm31 = dm32 + ordering * dmSq21
    return dm31

converters = dict(
        amplitude13=dict(single=amplitude_single_double, double=unity),
        amplitude23=dict(single=amplitude_single_double, double=unity),
        dm32={
            '32': unity,
            '32NO': dm32_from_32NO,
            '32NO/31IO': dm32_from_32NO_31IO,
            'ee': dm32_from_ee,
            '31': dm32_from_31,
            'avg' : dm32_from_avg
        },
        dm31={
            '31': unity,
            '32NO/31IO': dm31_from_32NO_31IO,
            'ee': dm31_from_ee,
            '32': dm31_from_32,
            'avg' : dm31_from_avg
        }
        )

def convert(var, mode, *vals, **kwargs):
    try:
        fcn = converters[var][mode]
    except KeyError:
        raise Exception(f'Do not know how to convert {var} {mode}')

    def converter(val):
        return fcn(val, **kwargs)

    return map(converter, vals)


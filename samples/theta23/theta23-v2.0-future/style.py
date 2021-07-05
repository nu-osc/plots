colors = {
        'junoreactor':     'xkcd:red',
        'junosolar':       'xkcd:saffron',
        'junoatmospheric': 'xkcd:azure',
        'kamland':         'xkcd:red',
        'kamlandsksno':    'xkcd:azure',
        'nova':            'xkcd:green',
        't2k':             'xkcd:green',
        'minos':           'xkcd:green',
        'superkamiokande': 'xkcd:azure',
        'icecube':         'xkcd:azure',
        'nufit5.0':        'xkcd:steel grey',
        'foreroetal.':     'xkcd:steel grey'
        }

names = {
        'Super-Kamiokande': 'SuperK',
        # 'JUNO atmospheric': r'\textbf{JUNO} {\relscale{0.8}\FilledRainCloud} \relsize{-2}(expected)'
        # 'JUNO atmospheric': r'\textbf{JUNO} {\relscale{0.9}\raisebox{1.5mm}{\FilledCloud}{\relscale{0.5}\hspace{-5mm}\raisebox{-0.7mm}{\Lightning\hspace{-0.8mm}\Lightning}}} \relsize{-2}(expected)', # ifsym
        'JUNO atmospheric': r'\textbf{JUNO} {\relscale{0.9}\raisebox{1.5mm}{\Cloud}{\relscale{0.8}\hspace{-4.7mm}\raisebox{-1.1mm}{\Lightning\hspace{-0.0mm}\Lightning}}} \relsize{-2}(expected)'
        }

preamble = r'\usepackage[weather]{ifsym}\let\Lightning\undefined\let\Sun\undefined\usepackage{marvosym}\usepackage{relsize}'

titles = dict(
    NO='Normal mass ordering',
    IO='Inverted mass ordering',
    )

colors = {
        'reactor':     'xkcd:red',
        'reacsolar':   'xkcd:orange',
        'solar':       'xkcd:saffron',
        'atm':         'xkcd:azure',
        'acc':         'xkcd:green',
        'global':      'xkcd:steel gray',
        }

colors = {
    'kamland':         colors['reactor'],
    'reno_ngd':        colors['reactor'],
    'reno_nh':         colors['reactor'],
    'dayabay_ngd':     colors['reactor'],
    'dayabay_nh':      colors['reactor'],
    'doublechooz':     colors['reactor'],
    'dchooz':          colors['reactor'],
    'kamlandsksno':    colors['reacsolar'],
    'nova':            colors['acc'],
    't2k':             colors['acc'],
    'minos':           colors['acc'],
    'superkamiokande': colors['atm'],
    'superksno':       colors['solar'],
    'sno':             colors['solar'],
    'icecube':         colors['atm'],
    'nufit5.1':        colors['global'],
    'foreroetal.':     colors['global'],
    'junoreactor':     colors['reactor'],
    'junoreactor_nh':  colors['reactor'],
    'junoreactor_ih':  colors['reactor'],
    'dune':            colors['acc'],
    'orca':            colors['atm'],
    'hyperkamiokande': colors['acc'],
    'ino':             colors['atm'],
    'icecubeupgrade':  colors['atm'],
    'essnusb':         colors['acc'],
    'junoatmospheric': colors['atm'],
    }

names = {
        'Super-Kamiokande': 'SuperK',
        'Hyper-Kamiokande': 'HyperK',
        # 'JUNO atmospheric': r'\textbf{JUNO} {\relscale{0.8}\FilledRainCloud} \relsize{-2}(expected)'
        # 'JUNO atmospheric': r'\textbf{JUNO} {\relscale{0.9}\raisebox{1.5mm}{\FilledCloud}{\relscale{0.5}\hspace{-5mm}\raisebox{-0.7mm}{\Lightning\hspace{-0.8mm}\Lightning}}} \relsize{-2}(expected)', # ifsym
        'JUNO atmospheric': r'JUNO',
        'ESSnuSB': r'ESS$\nu$SB'
        }

preamble = r'\usepackage[weather]{ifsym}\let\Lightning\undefined\let\Sun\undefined\usepackage{marvosym}\usepackage{relsize}'

titles = dict(
    NO='Normal mass ordering',
    IO='Inverted mass ordering',
    )

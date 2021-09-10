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
    'nufit5.0':        colors['global'],
    'foreroetal.':     colors['global'],
    'junoreactor':     colors['reactor'],
    'junoreactor_nh':  colors['reactor'],
    'junoreactor_ih':  colors['reactor'],
    'dune':            colors['acc'],
    'orca':            colors['atm'],
    'hyperkamiokande': colors['acc'],
    'ino':             colors['atm'],
    'icecubeupgrade':  colors['atm'],
    'essnusb':         colors['acc']
	}

names = {
        'Super-Kamiokande': 'SuperK',
        'JUNO reactor': r'JUNO',
        'Hyper-Kamiokande': 'HyperK'
        }

preamble = r'\usepackage{marvosym}\usepackage{relsize}'

def dayabay():
	colors['dayabay_nh'] = 'xkcd:blue'
	colors['dayabay_ngd'] = 'xkcd:blue'

titles = dict(
    NO='Normal mass ordering',
    IO='Inverted mass ordering',
    )

version='4'
url='git.jinr.ru/nu/osc'
date='2022.06'
variable=r'$\sin^2 \theta_{12}$'
lims = (0.27, 0.355)

reference = f'v{version} {date}: {url}'

colors = {
    'junoreactor':     'xkcd:red',
    'junoreactor_ih':  'xkcd:red',
    'junoreactor_nh':  'xkcd:red',
    'junosolar':       'xkcd:saffron',
    'kamland':         'xkcd:red',
    'kamlandsksno':    'xkcd:orange',
    'nova':            'xkcd:green',
    't2k':             'xkcd:green',
    'minos':           'xkcd:green',
    'superksno':       'xkcd:saffron',
    'sno':             'xkcd:saffron',
    'icecube':         'xkcd:azure',
    'nufit5.1':        'xkcd:steel grey',
    'foreroetal.':     'xkcd:steel grey',
    'hyperkamiokande': 'xkcd:saffron',
    'dune':            'xkcd:saffron',
    'capozzietal.':    'xkcd:steel grey'
	}

names = {
	'Super-Kamiokande': 'SuperK+SNO',
	'JUNO solar':   r'JUNO {\relscale{0.75}\SunshineOpenCircled} + SNO(NC)',
	'JUNO reactor': r'JUNO \Radioactivity{}',
    'Hyper-Kamiokande': 'HyperK+SNO+SK',
	}

preamble = r'\usepackage{bbding}\let\Cross\undefined\usepackage{marvosym}\usepackage{relsize}'

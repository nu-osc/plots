version='2.0'
url='git.jinr.ru/nu/osc'
date='2021.07'
variable=r'$\sin^2 \theta_{12}$'
lims = (0.28, 0.36)
scale = 10.0
width_value='20mm'
width_error='10mm'
plot_fbox=False
relsize_relerror=-2

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
    'nufit5.0':        'xkcd:steel grey',
    'foreroetal.':     'xkcd:steel grey'
	}

names = {
	'Super-Kamiokande': 'SuperK+SNO',
	'JUNO solar':   r'JUNO {\relscale{0.75}\SunshineOpenCircled}+SNO(NC) \hspace{9cm}\relsize{-2}(expected)',
	'JUNO reactor': r'JUNO \Radioactivity{} \relsize{-2}(expected)'
	}

preamble = r'\usepackage{bbding}\let\Cross\undefined\usepackage{marvosym}\usepackage{relsize}'

import matplotlib as mpl
mpl.rc_file('matplotlib.rc')

version='0.1'
url='git.jinr.ru/nu/osc'
date='2020.12'
reference = f'v{version} {date}: {url}'

xlabel=r'$|\Delta m^2_{32}|$ NO, $10^{-3}$ eV$^2$'

styles = {
	'reactor':     { 'color': 'red' },
	'accelerator': { 'color': 'green' },
	}

styles.update({
    'Daya Bay':     styles['reactor'],
    'RENO':         styles['reactor'],
    'Double CHOOZ': styles['reactor'],
    'T2K':          styles['accelerator'],
    'NOvA':         styles['accelerator'],
    'MINOS':        styles['accelerator'],
    'MINOS+':       styles['accelerator'],
    'T2K NO':       styles['accelerator'],
    'T2K IO':       styles['accelerator'],
    })

styles.update({
    'Daya Bay':    { 'color': 'blue', 'linewidth': 2.0 },
})

texstyles = {
	'Daya Bay': r'\bf{}'
	}

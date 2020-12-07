import matplotlib as mpl
mpl.rc_file('matplotlib.rc')

xlabel=r'$\sin^2 2\theta_{13}$'

styles = {
	'reactor':     { 'color': 'red' },
	'accelerator': { 'color': 'green' },
	}

styles.update({
    'Daya Bay':     styles['reactor'],
    'RENO':         styles['reactor'],
    'Double CHOOZ': styles['reactor'],
    'T2K':          styles['accelerator']
    })

styles.update({
    'Daya Bay':    { 'color': 'blue', 'linewidth': 2.0 },
})

texstyles = {
	'Daya Bay': r'\bf{}'
	}

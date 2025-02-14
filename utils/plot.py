import matplotlib.pyplot as plt
import os
import numpy as np


def plot(*dice, draw_mean=False, show_plot=True, title=None, save_plot=False, overwrite_file=False, mode='normal'):
	plt.figure(figsize=(16, 9), dpi=80)
	plt.rc(
		'lines',
		linewidth=3,
		marker='o',
		markersize=8,
		markeredgewidth=0,
	)

	color_index = 0
	dice_count = 1
	for die in dice:
		if isinstance(die, tuple):
			die, name = die
		else:
			name = "plot {}".format(dice_count)
			dice_count += 1
		__plot_single_die(color_index, (die, name), draw_mean=draw_mean, mode=mode)
		color_index = (color_index + 1) % len(color_list)

	# figure = plt.figure() # TODO: improve pyplot usage
	plt.xlabel('dice roll value')
	plt.ylabel('likelihood (in percent)')
	plt.title('Dice' if title is None else title)
	plt.ylim(ymin=0)
	plt.legend(loc='upper right')
	plt.grid(True)

	if save_plot:
		if not isinstance(save_plot, str):
			if title is not None:
				save_plot = title
			else:
				raise ValueError("No filename specified to save plot. Use either 'title=\"name.png\"' or 'save_plot=\"name.png\"'")
		if not overwrite_file and os.path.isfile(save_plot):
			message = "The file '{}' already exists. Use 'overwrite_file=True' to overwrite or use another name.".format(save_plot)
			raise FileExistsError(message)
		elif os.path.isdir(save_plot):
			message = "'{}' is a directory, use another name.".format(save_plot)
			raise IsADirectoryError(message)
		else:
			plt.savefig(save_plot)

	if show_plot:
		plt.show()


def __plot_single_die(color_index, die_data, draw_mean=False, mode='normal'):
	die, name = die_data
	xdata = die.values()
	_ydata = die.expectancies()
	if mode in plot_modes.keys():
		ydata = plot_modes[mode](_ydata)
	else:
		raise ValueError('No such mode available: {}. Available modes: {}'.format(mode, ', '.join(plot_modes.keys())))
	mean, std_dev = die.mean_and_std_dev()
	label = '{name} ({mean:.2f}, {std:.2f})'.format(name=name, mean=mean, std=std_dev)
	color = color_list[color_index]
	plt.plot(
		xdata,
		ydata,
		color=color,
		label=label
	)
	if draw_mean:
		mean, mean_expectancy = die.mean_value_and_expectancy()
		plt.plot(
			mean,
			mean_expectancy * 100,
			color=color,
			markersize=9,
			markeredgewidth=1
		)

colors = {
	"""
	The HEX values of these colors are taken from Ethan Schoonover's Solarized theme (http://ethanschoonover.com/solarized)
	"""
	'yellow': '#b58900',
	'orange': '#cb4b16',
	'red': '#dc322f',
	'magenta': '#d33682',
	'violet': '#6c71c4',
	'blue': '#268bd2',
	'cyan': '#2aa198',
	'green': '#859900',
	'black': '#000000',
}
nice_colors = [
	'#003f5c',
	'#ef5675',
	'#7a5195',
	'#ff764a',
	'#374c80',
	'#bc5090',
	'#ffa600'
]

# color_list = list(colors.values())
color_list = nice_colors



plot_modes = {
	'normal': lambda ydata: ydata*100,
	'atLeast': lambda ydata: np.array([ydata[i:].sum() for i in np.arange(len(ydata))])*100,
	'atMost': lambda ydata: np.array([ydata[:i+1].sum() for i in np.arange(len(ydata))])*100
}

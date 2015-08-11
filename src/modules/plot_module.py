import itertools
import matplotlib
import matplotlib.pyplot as plt

from ..baseplot import BasePlot
BasePlot.init_matplotlib()

from ..baseplot import plot_errorbar, plot_band, plot_line, add_axis_text
from ..root2mpl import MplObject1D
from modules import Module


class PlotModule(Module):
    def __init__(self):
        super(PlotModule, self).__init__()
        # Plot object options
        self.parser.add_argument('--label', type='str2kvstr', nargs='+', default=['__nolegend__'], action='setting',
                                 help='Legend labels for each plot')
        self.parser.add_argument('--color', type='str2kvstr', nargs='+',
                                 default='auto', action='setting',
                                 help='Colors for each plot')
        self.parser.add_argument('--edgecolor', type='str2kvstr', nargs='+',
                                 default='auto', action='setting',
                                 help='Edgecolor for each plot')
        self.parser.add_argument('--hatch', type='str2kvstr', nargs='+',
                                 default=None, action='setting',
                                 help='Hatch for each plot')
        self.parser.add_argument('--linestyle', type='str2kvstr', nargs='+',
                                 default='', action='setting',
                                 help='Linestyle for each plot')
        self.parser.add_argument('--marker', type='str2kvstr', nargs='+',
                                 default='.', action='setting',
                                 help='Marker for errorbars for each plot.')
        self.parser.add_argument('--x-err', type='str2kvbool', nargs='+', default=True, action='setting',
                                 help='Show x-errors.')
        self.parser.add_argument('--y-err', type='str2kvbool', nargs='+', default=True, action='setting',
                                 help='Show y-errors.')
        self.parser.add_argument('--alpha', type='str2kvfloat', nargs='+', default=1.0, action='setting',
                                 help='Alpha value in plot.')
        self.parser.add_argument('--capsize', type='str2kvint', nargs='+', default=0, action='setting',
                                 help='Capsize of errorbars in plot.')
        self.parser.add_argument('--zorder', type='str2kvfloat', nargs='+', default=1.0, action='setting',
                                 help='Alpha value in plot.')
        self.parser.add_argument('--style', default='errorbar', type='str2kvstr', nargs='+', action='setting',
                                 help='Style of the plotted object.')
        self.parser.add_argument('--step', type='str2kvbool', nargs='+', default=False, action='setting',
                                 help='Plot the data stepped at the xerr edges.')
        # Figure options
        self.parser.add_argument('--fig-size', type=float, nargs=2, default=None, help='Size of figure.')
        self.parser.add_argument('--output-path', default='plot.png', help='Path to output file.')
        self.parser.add_argument('--output-prefix', default='plots/', help='Prefix to output paths.')

        # Axis options
        self.parser.add_argument('--x-lims', nargs=2, default=[None, None], help='X limits of plot.')
        self.parser.add_argument('--y-lims', nargs=2, default=[None, None], help='Y limits of plot.')

        self.parser.add_argument('--x-log', default=False, type='bool', help='Show x-errors.')
        self.parser.add_argument('--y-log', default=False, type='bool', help='Show y-errors.')

        self.parser.add_argument('--x-label', default='', help='xlabel')
        self.parser.add_argument('--y-label', default='', help='ylabel')

        self.parser.add_argument('--show-legend', type='bool', default=True, help='Show a legend.')
        self.parser.add_argument('--legend-loc', default='best', help='Legend location.')

        self.parser.add_argument('--ax-texts', nargs='+', default=[],
                                 help='Add text to plot. Syntax is \'Text?1.0,1.0\' with loc 1.0,1.0')
        self.parser.add_argument('--ax-vlines', nargs='+', default=[],
                                 help='Add vertical lines to plot. Syntax is y_pos?color?lw.')
        self.parser.add_argument('--ax-hlines', nargs='+', default=[],
                                 help='Add horizontal lines to plot. Syntax is y_pos?color?lw.')


    def __call__(self, config):
        plot = Plot(**config)
        # plot each object
        for id, item in config['objects'].iteritems():
            if not id.startswith('_'):
                plot.plot(**item)
        # Save plot
        plot.finish()


def get_plot(*args, **kwargs):
    return Plot(*args, **kwargs)


class Plot(BasePlot):
    def __init__(self, histos=None, **kwargs):

        super(Plot, self).__init__(**kwargs)
        self.ax = self.fig.add_subplot(111)
        self.histos = histos

        self.x_lims = kwargs.pop('x_lims', (None, None))
        self.x_lims = [any2float(v) for v in self.x_lims]
        self.y_lims = kwargs.pop('y_lims', (None, None))
        self.y_lims = [any2float(v) for v in self.y_lims]

        self.x_log = kwargs.pop('x_log', False)
        self.y_log = kwargs.pop('y_log', False)

        self.x_label = kwargs.pop('x_label', '')
        self.y_label = kwargs.pop('y_label', '')

        self.show_legend = kwargs.pop('show_legend', True)
        self.legend_loc = kwargs.pop('legend_loc', 'best')

        self.texts = kwargs.pop('ax_texts', [])
        self.vlines = kwargs.pop('ax_vlines', [])
        self.hlines = kwargs.pop('ax_hlines', [])

        self.auto_colors = itertools.cycle(matplotlib.rcParams['axes.color_cycle'])

    def plot(self, **kwargs):
        kwargs['obj'] = MplObject1D(kwargs.get('obj'))
        style = kwargs.pop('style', 'errorbar')

        if kwargs['color'] == 'auto':
            kwargs['color'] = next(self.auto_colors)
        if kwargs['edgecolor'] == 'auto':
            kwargs['edgecolor'] = kwargs['color']

        if style == 'errorbar':
            artist = plot_errorbar(ax=self.ax, **kwargs)
        elif style == 'band':
            artist = plot_band(ax=self.ax, **kwargs)
        elif style == 'line':
            artist = plot_line(ax=self.ax, **kwargs)
        else:
            raise ValueError('Style {0} not supported.'.format(style))
        return artist

    def make_plots(self):

        for i, histo in enumerate(self.histos):
            self.plot(histo)

    def finish(self):

        # Add axis texts
        for text in self.texts:
            text, loc = text.rsplit('?', 1)
            add_axis_text(self.ax, text, loc=loc)

        # Add horizontal lines to ax
        for hline in self.hlines:
            ypos, color, lw = hline.split('?')
            self.ax.axhline(y=float(ypos), color=color, lw=lw, zorder=0.99)
        # Add vertical lines to ax
        for vline in self.vlines:
            xpos, color, lw = vline.split('?')
            self.ax.axvline(y=float(ypos), color=color, lw=lw)

        self.ax.set_ylim(ymin=self.y_lims[0], ymax=self.y_lims[1])
        self.ax.set_xlim(xmin=self.x_lims[0], xmax=self.x_lims[1])

        self.ax.set_xlabel(self.x_label, position=(1., 0.), va='top', ha='right')
        self.ax.set_ylabel(self.y_label)

        self.ax.set_xscale('log' if self.x_log else 'linear')
        self.ax.set_yscale('log' if self.y_log else 'linear')

        if self.show_legend:
            self.ax.legend(loc=self.legend_loc)

        self.save_fig()
        plt.close(self.fig)


def str2bool(v):
    """ Parse string content to bool."""
    return v.lower() in ("yes", "true", "t", "1")


def any2float(v):
    """Return float if parseable, else None."""
    try:
        return float(v)
    except (TypeError, ValueError):
        return None

import os
from abc import ABCMeta, abstractmethod
from root2mpl import MplObject1D
import numpy as np

import matplotlib
from matplotlib.colors import Normalize
from matplotlib.colors import LogNorm
import matplotlib.pyplot as plt


class BasePlot(object):
    __metaclass__ = ABCMeta

    def __init__(self, **kwargs):

        self.init_matplotlib()

        figsize = kwargs.pop('figsize', None)
        if figsize:
            self.fig = plt.figure(figsize=figsize)
        else:
            self.fig = plt.figure()

        self.output_path = kwargs.pop('output_path', 'plot.png')
        self.output_folder = kwargs.pop('output_folder', 'plots')

    def save_fig(self, close_fig=True):
        """
        Save Fig to File and create directory structure
        if not yet existing.
        """
        #Check if directory exists and create if not
        directory = os.path.dirname(self.output_path)

        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        # for ext in self.output_ext:
            # if not m.lower().endswith(('.png', '.jpg', '.jpeg', '.pdf', '.ps'))
            # filename = "{}.{}".format(self.output_path, ext)
        print 'Saved plot to {0}'.format(self.output_path)
        self.fig.savefig(self.output_path, bbox_inches='tight')

        if close_fig:
            plt.close(self.fig)

    @staticmethod
    def init_matplotlib():
        """
        Initialize matplotlib with rc settings.
        """
        # figure
        matplotlib.rcParams['figure.figsize'] = 10., 10.

        matplotlib.rcParams['lines.linewidth'] = 2
        matplotlib.rcParams['font.family'] = 'sans-serif'
        matplotlib.rcParams['font.serif'] = 'lmodern'
        matplotlib.rcParams['font.sans-serif'] = 'Helvetica'
        matplotlib.rcParams['font.monospace'] = 'Computer Modern Typewriter'
        matplotlib.rcParams['font.style'] = 'normal'
        matplotlib.rcParams['font.size'] = 20.
        matplotlib.rcParams['legend.fontsize'] = 14.
        matplotlib.rcParams['text.usetex'] = False
        # matplotlib.rc('text.latex', preamble=r'\usepackage{helvet},\usepackage{sfmath}')
        # matplotlib.rc('text.latex', preamble=r'\usepackage{helvet}')
        # Axes
        matplotlib.rcParams['axes.linewidth'] = 2
        matplotlib.rcParams['axes.labelsize'] = 20
        matplotlib.rcParams['xtick.labelsize'] = 16
        matplotlib.rcParams['xtick.major.size'] = 8
        matplotlib.rcParams['xtick.major.width'] = 1.5
        matplotlib.rcParams['xtick.minor.size'] = 6
        matplotlib.rcParams['xtick.minor.width'] = 1.
        matplotlib.rcParams['ytick.labelsize'] = 16
        matplotlib.rcParams['ytick.major.width'] = 1.5
        matplotlib.rcParams['ytick.major.size'] = 8
        matplotlib.rcParams['ytick.minor.size'] = 6
        matplotlib.rcParams['ytick.minor.width'] = 1.
        matplotlib.rcParams['lines.markersize'] = 8

        # Saving
        matplotlib.rcParams['savefig.bbox'] = 'tight'
        matplotlib.rcParams['savefig.dpi'] = 150
        matplotlib.rcParams['savefig.format'] = 'png'
        matplotlib.rcParams['agg.path.chunksize'] = 20000

        # default color cycle
        matplotlib.rcParams['axes.color_cycle'] = ['#1f77b4',
                                                   '#ff7f0e',
                                                   '#2ca02c',
                                                   '#d62728',
                                                   '#9467bd',
                                                   '#8c564b',
                                                   '#e377c2',
                                                   '#7f7f7f',
                                                   '#bcbd22',
                                                   '#17becf']

        matplotlib.rcParams["axes.formatter.limits"] = [-5, 5]
        # legend
        matplotlib.rcParams['legend.numpoints'] = 1
        matplotlib.rcParams['legend.fontsize'] = 19
        matplotlib.rcParams['legend.labelspacing'] = 0.3
        matplotlib.rcParams['legend.frameon'] = False
        # Saving
        matplotlib.rcParams['savefig.bbox'] = 'tight'
        matplotlib.rcParams['savefig.dpi'] = 150
        matplotlib.rcParams['savefig.format'] = 'png'
        matplotlib.rcParams['agg.path.chunksize'] = 20000
    #
    # Helper functions
    #

    def set_style(self, ax, style, show_cme=False):
        """
        Some preset styles
        """
        if style == 'none':
            pass
        elif style == 'cmsprel':
            self.set_preset_text(ax, r"\textbf{CMS Preliminary}", loc='topleft')
            if show_cme:
                self.set_preset_text(ax, r"$\sqrt{s} = 7\/ \mathrm{TeV}$",
                                     loc='topleft', )
        else:
            self.set_preset_text(ax, r"\textbf{CMS}", loc='topleft')
            if show_cme:
                self.set_preset_text(ax, r"$\sqrt{s} = 7\/ \mathrm{TeV}$",
                                     loc='topleft', )

def add_axis_text(ax, text, loc='top right', **kwargs):
    """
    Possible Positions : top left, top right
    """
    if loc == 'top left':
        kwargs.update({'x': 0.0, 'y': 1.01, 'va': 'bottom',
                       'ha': 'left'})
    elif loc == 'top right':
        kwargs.update({'x': 1.0, 'y': 1.01, 'va': 'bottom',
                       'ha': 'right'})
    elif ',' in loc:
        x, y = map(float, loc.split(','))
        kwargs.update({'x': x, 'y': y, 'va': 'bottom',
                       'ha': 'left'})
    else:
        raise Exception('Unknown loc.')

    ax.text(s=text, transform=ax.transAxes, **kwargs)


def autoscale(ax, xmargin=0.0, ymargin=0.0, margin=0.0):
    # User defined autoscale with margins
    x0, x1 = tuple(ax.dataLim.intervalx)
    if margin > 0:
        xmargin = margin
        ymargin = margin
    if xmargin > 0:
        if ax.get_xscale() == 'linear':
            delta = (x1 - x0) * xmargin
            x0 -= delta
            x1 += delta
        else:
            delta = (x1 / x0) ** xmargin
            x0 /= delta
            x1 *= delta
        ax.set_xlim(x0, x1)
    y0, y1 = tuple(ax.dataLim.intervaly)
    if ymargin > 0:
        if ax.get_yscale() == 'linear':
            delta = (y1 - y0) * ymargin
            y0 -= delta
            y1 += delta
        else:
            delta = (y1 / y0) ** ymargin
            y0 /= delta
            y1 *= delta
        ax.set_ylim(y0, y1)

def log_locator_filter(x, pos):
    """
    Add minor tick labels in log plots at 2* and 5*
    """
    s = str(int(x))
    if len(s) == 4:
        return ''
    if s[0] in ('2', '5'):
        return '${0}$'.format(s)
    return ''


def set(obj, *args, **kwargs):
    """
    Apply Settings in kwargs, while defaults are set
    """
    funcvals = []
    for i in range(0, len(args) - 1, 2):
        funcvals.append((args[i], args[i + 1]))
    funcvals.extend(kwargs.items())
    for s, val in funcvals:
        attr = getattr(obj, s)
        if callable(attr):
            attr(val)
        else:
            setattr(obj, attr, val)


def ensure_latex(inp_str):
    """
    Return string with escaped latex incompatible characters.
    :param inp_str:
    :return:
    """
    chars = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\letteropenbrace{}',
        '}': r'\letterclosebrace{}',
        '~': r'\lettertilde{}',
        '^': r'\letterhat{}',
        '\\': r'\letterbackslash{}',
    }
    return ''.join([chars.get(char, char) for char in inp_str])

def steppify_bin(arr, isx=False):
    """
    Produce stepped array of arr, needed for example for stepped fill_betweens.
    Pass all x bin edges to produce stepped x arr and all y bincontents to produce
    stepped bincontents representation
    steppify_bin([1,2,3], True) 
    -> [1,2,2,3]
    steppify_bin([5,6])
    -> [5,5,6,6]
    """
    if isx:
        newarr = np.array(zip(arr[:-1], arr[1:])).ravel()
    else:
        newarr = np.array(zip(arr, arr)).ravel()
    return newarr


def plot_band(obj, step=False, emptybins=True, ax=None, **kwargs):
    """ Produce an errorbar plots with or without connecting lines.

    Args:
        obj: Mplobj representation of a root object.
        ax: Axis to plot on. If not specified current global axis will be used.
        show_xerr: If True, x errorbars will be plotted.
        show_yerr: If True, y errorbars will be plotted.
        emptybins: Not Implemented. Supposed to ignore/plot empty bins.
    """

    # if no axis passed use current global axis
    if ax is None:
        ax = plt.gca()


    color = kwargs.pop('color', next(ax._get_lines.color_cycle))
    label = kwargs.pop('label', '')

    x = obj.x
    y = obj.y
    yerrl = obj.yerrl
    yerru = obj.yerru
    if step:
        x = steppify_bin(obj.xbinedges, isx=True)
        y = steppify_bin(y)
        yerrl = steppify_bin(yerrl)
        yerru = steppify_bin(yerru)

    label = kwargs.pop('label', '')
    artist = ax.fill_between(x, y-yerrl, y+yerru, label=label, color=color, **kwargs)
    return artist



def plot_errorbar(obj, step=False, show_xerr=True, show_yerr=True, emptybins=True, ax=None, **kwargs):
    """ Produce an errorbar plots with or without connecting lines.

    Args:
        obj: Mplobj representation of a root objogram.
        ax: Axis to plot on. If not specified current global axis will be used.
        show_xerr: If True, x errorbars will be plotted.
        show_yerr: If True, y errorbars will be plotted.
        emptybins: Not Implemented. Supposed to ignore/plot empty bins.
    """

    # if no axis passed use current global axis
    if ax is None:
        ax = plt.gca()

    x = obj.x
    y = obj.y

    if show_xerr:
        xerr = np.array((obj.xerrl, obj.xerru))
    else:
        xerr = None
    if show_yerr:
        yerr = np.array((obj.yerrl, obj.yerru))
    else:
        yerr = None

    linestyle = kwargs.pop('linestyle', '')
    color = kwargs.pop('color', next(ax._get_lines.color_cycle))
    capsize = kwargs.pop('capsize', 0)
    fmt = kwargs.pop('fmt', '')
    if fmt in ['bar', 'fill']:
        log.warning('Invalid marker style. Default to \'.\'')
        fmt = '.'
    label = kwargs.pop('label', '')
    # Due to a bug in matplotlib v1.1 errorbar does not always respect linestyle when fmt is passed.
    # Workaround by plotting line and errorbars separately.
    # http://stackoverflow.com/a/18499120/3243729
    if linestyle:
        if step:
            ax.step(steppify_bin(obj.xbinedges, isx=True), steppify_bin(y), linestyle=linestyle, color=color, **kwargs)
        else:
            ax.plot(x, y, linestyle=linestyle, color=color, **kwargs)
    artist = ax.errorbar(x, y, xerr=xerr, yerr=yerr, label=label, capsize=capsize, fmt=fmt, linestyle='None', color=color, **kwargs)
    return artist


def plot_contour1d(hist, ax=None, z_log=False, vmin=None, vmax=None, cmap='afmhot'):
    """One dimensional contour plot.
    Args:
        hist: MplHisto representation of a root histogram.
        ax: Axis to plot on. If not specified current global axis will be used.
        z_log: If True, z axis will be logarithmic.
        vmin: Lower limit of z axis
        vmax: Upper limit of z axis
        cmap: Colormap used to
    """
    cmap = matplotlib.cm.get_cmap(cmap)
    if ax is None:
        ax = plt.gca()
    if (vmin, vmax) == (None,)*2:
        if z_log:
            vmin, vmax = np.min(hist.bincontents[np.nonzero(hist.bincontents)]), np.amax(hist.bincontents)
        else:
            vmin, vmax = np.amin(hist.bincontents), np.amax(hist.bincontents)
    norm = (LogNorm if z_log else Normalize)(vmin=vmin, vmax=vmax)

    # special settings for masked arrays (TProfile2Ds):
    if type(hist.bincontents) == np.ma.core.MaskedArray:
        min_color, max_color = cmap(norm(vmin))[:3], cmap(norm(vmax))[:3]  # get min and max colors from colorbar as rgb-tuples

        # set color for masked entries depending on min and max color of colorbar
        mask_color = 'white'
        if any([all([i>0.95 for i in color]) for color in [min_color, max_color]]):  # check if white is min or max color
            mask_color = 'black'
            if any([all([i<0.05 for i in color]) for color in [min_color, max_color]]):  # check if black is min or max color
                mask_color = 'red'
        cmap.set_bad(mask_color, alpha=None)
    if z_log:
        cmap.set_bad('gray', alpha=None)
    artist = ax.pcolormesh(hist.xbinedges, hist.ybinedges, hist.bincontents, cmap=cmap, norm=norm)
    return artist

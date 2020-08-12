
import logging
import warnings
import matplotlib.colors as mcolors
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd
from bidi import algorithm as bidialg
from matplotlib.lines import Line2D
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from pandas.plotting import register_matplotlib_converters

from contagiograms import consts

register_matplotlib_converters()
warnings.simplefilter("ignore")
logger = logging.getLogger(__name__)


def plot_contagiograms(savepath, ngrams, t1, t2, shading, fullpage):
    """ Plot a grid of contagiograms

    Args:
        savepath: path to save plot
        ngrams: a 2D-list of ngrams to plot
        t1: time scale to investigate relative social amplification [eg, M, 2M, 6M, Y]
        t2: window size for smoothing the main timeseries [days]
        shading: a toggle to either shade the area between the min and max or plot individual lines
        fullpage: a toggle to switch to 3 columns instead of 2
        saves a figure to {savepath}
    """

    plt.rcParams.update({
        'font.size': 10,
        'axes.titlesize': 14,
        'axes.labelsize': 12,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'legend.fontsize': 10,
    })
    size = 6
    r = len(ngrams)//3 if fullpage else len(ngrams)//2

    if len(ngrams) == 1:
        cols = 1
        rows = size
    else:
        cols = 3 if fullpage else 2
        rows = (r * size) + r if fullpage else (r * size) + r

    if len(ngrams) == 1:
        figsize = (4, 4)
    elif len(ngrams) == 2:
        figsize = (8, 6)
    else:
        figsize = (12, size+(2*r+2)) if fullpage else (8, size+(2*r))

    fig = plt.figure(figsize=figsize)
    gs = fig.add_gridspec(ncols=cols, nrows=rows)
    metric = 'rank'
    labels = 'A B C D E F G H I J K L M N O P Q R S T U V W X Y Z'.split(' ')
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    vmin, vmax, vcenter, step = 0, 2, 1, .1
    contagion_color = 'orangered'
    rtcmap = plt.get_cmap('OrRd', 256)
    otcmap = plt.get_cmap('Greys_r', 256)

    cmap = np.vstack((
        otcmap(np.linspace(.4, 1-step, int(abs(vcenter - vmin)/step))),
        [1, 1, 1, 1],
        rtcmap(np.linspace(0, 1+step, int(abs(vcenter - vmax)/step)))
    ))
    cmap = mcolors.ListedColormap(cmap)

    minr, maxr = 1, 10**6
    start_date = ngrams[0].index[0]
    end_date = ngrams[0].index[-1]
    diff = end_date - start_date

    if diff.days < 1000:
        major_format = '%b\n%Y'
        minor_format = '%b'
        major_locator = mdates.YearLocator()
        minor_locator = mdates.AutoDateLocator()

    else:
        major_format = '%Y'
        minor_format = ''
        major_locator = mdates.YearLocator(2)
        minor_locator = mdates.YearLocator()

    i = 0
    for r in np.arange(0, rows, step=size+1):
        for c in np.arange(cols):
            cax = fig.add_subplot(gs[r, c])
            langax = fig.add_subplot(gs[r+1:r+3, c])
            ax = fig.add_subplot(gs[r+3:r+size, c])

            df = ngrams[i]
            df.index = pd.to_datetime(df.index)
            df = df.dropna(how='all')

            start_date = df.index[0]
            end_date = df.index[-1]

            ax.set_xlim(start_date, end_date)
            cax.set_xlim(start_date, end_date)
            langax.set_xlim(start_date, end_date)

            ax.xaxis.set_major_locator(major_locator)
            ax.xaxis.set_major_formatter(mdates.DateFormatter(major_format))
            ax.xaxis.set_minor_locator(minor_locator)
            ax.xaxis.set_minor_formatter(mdates.DateFormatter(minor_format))

            cax.xaxis.set_major_locator(major_locator)
            cax.xaxis.set_major_formatter(mdates.DateFormatter(major_format))
            cax.xaxis.set_minor_locator(minor_locator)
            cax.xaxis.set_minor_formatter(mdates.DateFormatter(minor_format))

            langax.xaxis.set_major_locator(major_locator)
            langax.xaxis.set_major_formatter(mdates.DateFormatter(major_format))
            langax.xaxis.set_minor_locator(minor_locator)
            langax.xaxis.set_minor_formatter(mdates.DateFormatter(minor_format))

            df['count'] = df['count'].fillna(0)
            df['count_no_rt'] = df['count_no_rt'].fillna(0)

            df['freq'] = df['freq'].fillna(0)
            df['freq_no_rt'] = df['freq_no_rt'].fillna(0)

            df['rank'] = df['rank'].fillna(maxr)
            df['rank_no_rt'] = df['rank_no_rt'].fillna(maxr)

            alpha = (
                (df['count'] - df['count_no_rt']) / df['count']
            ) / ((df['lang_num_ngrams'] - df['lang_num_ngrams_no_rt']) / df['lang_num_ngrams'])
            alpha = alpha.replace([np.inf, -np.inf, np.nan], 1)

            at = df['count'].resample(t1).mean()
            ot = df['count_no_rt'].resample(t1).mean()
            rt = at - ot

            lang, word = df.index.name.split('\n')
            try:
                word = bidialg.get_display(word)
            except UnicodeEncodeError:
                word = str(word, 'utf-8')

            if not word.isascii() and lang in consts.fonts.keys():
                prop = consts.fonts.get(lang)
            else:
                prop = consts.fonts.get('Default')

            cax.text(
                .5,
                2.1,
                lang,
                horizontalalignment='center',
                verticalalignment='top',
                transform=cax.transAxes,
                fontsize=10,
                color='grey'
            )
            cax.text(
                .5,
                1.6,
                word,
                horizontalalignment='center',
                verticalalignment='top',
                fontproperties=prop,
                transform=cax.transAxes,
                fontsize=12,
            )

            try:
                # plot contagion fraction
                cax.fill_between(
                    rt.index, 0, 1,
                    where=(rt/at) >= .5,
                    facecolor=contagion_color,
                    alpha=.2
                )

                heatmap = np.zeros((7, rt.shape[0]))
                for m, month in enumerate(rt.index):
                    for d, day in enumerate(days):
                        ds = pd.to_datetime(pd.date_range(
                            start=month - pd.DateOffset(months=1),
                            end=month,
                            freq=f'W-{day.upper()}'
                        ).strftime('%Y-%m-%d').tolist())

                        heatmap[d, m] = np.mean(alpha.loc[df.index.isin(ds)])

                mesh = langax.pcolormesh(
                    rt.index,
                    np.arange(8),
                    heatmap,
                    vmin=vmin,
                    vmax=vmax,
                    cmap=cmap,
                )

                langax.invert_yaxis()
                langax.set_yticks(np.arange(7))
                langax.set_yticklabels(days, fontsize=8)

                langax.set_xticklabels([], minor=False)
                langax.set_xticklabels([], minor=True)

                cax.plot(
                    ot / at,
                    lw=1,
                    color=consts.types_colors['OT']
                )
                cax.plot(
                    rt / at,
                    lw=1,
                    color=consts.types_colors['RT']
                )

                ax.plot(
                    df[metric].idxmin(), df[metric].min(),
                    'o', ms=8,
                    color='lightcoral',
                    mfc='lightcoral',
                    mec='lightcoral',
                )
                ax.plot(
                    df[metric].idxmin(), df[metric].min(),
                    'o', ms=1,
                    color='k',
                    mfc='k',
                    mec='k',
                )

                # plot timeseries
                if shading:
                    ts = df[metric].resample('W')
                    ax.fill_between(
                        ts.mean().index,
                        y1=ts.max(),
                        y2=ts.min(),
                        color='lightgrey',
                        facecolor='lightgrey',
                        edgecolor='lightgrey',
                        zorder=0,
                    )
                else:
                    ax.plot(
                        df[metric],
                        color='lightgrey',
                        lw=1,
                        zorder=0,
                    )

                ax.plot(
                    df[metric].rolling(t2, center=True).mean(),
                    color='k',
                    lw=1,
                )

            except ValueError as e:
                logger.warning(f'Value error for {df.index.name}: {e}.')

            ax.grid(True, which="both", axis='both', alpha=.3, lw=1, linestyle='-')
            cax.grid(True, which="both", axis='both', alpha=.3, lw=1, linestyle='-')
            langax.grid(True, which="both", axis='x', alpha=.3, lw=1, linestyle='-')
            langax.grid(True, which="major", axis='y', alpha=1, lw=1, linestyle='-', color='k')

            cax.set_xticklabels([], minor=False)
            cax.set_xticklabels([], minor=True)

            ax.set_ylim(minr, maxr)
            ax.invert_yaxis()
            ax.set_yscale('log')
            ax.yaxis.set_major_locator(
                ticker.LogLocator(base=10, numticks=12)
            )
            ax.set_yticks(
                [1, 10, 10**2, 10**3, 10**4, 10**5, 10**6],
                minor=False
            )
            ax.set_yticklabels(
                ['1', '10', '100', r'$10^3$', r'$10^4$', r'$10^5$', r'$10^6$'],
                minor=False
            )
            ax.yaxis.set_minor_locator(
                ticker.LogLocator(base=10.0, subs=np.arange(.1, 1, step=.1), numticks=30)
            )

            cax.set_ylim(0, 1)
            cax.set_yticks([0, .5, 1])
            cax.set_yticklabels(['0', '.5', '1'])
            cax.axhline(.5, color='k', lw=1)
            cax.spines['right'].set_visible(False)
            cax.spines['left'].set_visible(False)

            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_visible(False)
            ax.spines['top'].set_visible(False)

            langax.spines['top'].set_visible(False)
            langax.spines['right'].set_visible(False)
            langax.spines['left'].set_visible(False)
            langax.spines['bottom'].set_visible(False)
            langax.tick_params(axis='y', which='both', length=0)
            langax.set_yticklabels(days, va="top")

            if cols > 1:
                cax.annotate(
                    labels[i], xy=(-.15, 1.25), color='k', weight='bold',
                    xycoords="axes fraction", fontsize=16,
                )

            if c == cols-1:
                cax.legend(
                    handles=[
                        Line2D([0], [0], color=consts.types_colors['OT'], lw=2, label=r'OT'),
                        Line2D([0], [0], color=consts.types_colors['RT'], lw=2, label=r'RT'),
                    ],
                    loc='center right',
                    bbox_to_anchor=(1.2, .5),
                    ncol=1,
                    frameon=False,
                    fontsize=8,
                )

                cbarax = inset_axes(
                    langax,
                    width="3%",
                    height="100%",
                    bbox_to_anchor=(.075, .1, 1, 1),
                    bbox_transform=langax.transAxes,
                )
                plt.colorbar(
                    mesh,
                    cmap=cmap,
                    cax=cbarax,
                    orientation='vertical',
                    extend='max',
                    ticks=range(vmax+1)
                )

                cbarax.yaxis.set_label_position('right')

            if c == 0:
                x = -.22
                langax.text(
                    x, 0.5, r"$R^{\mathsf{rel}}_{\tau,t,\ell}$",
                    ha='center', fontsize=14,
                    verticalalignment='center', transform=langax.transAxes
                )

                cax.text(
                    x, 0.5, f"RT/OT\nBalance", ha='center',
                    verticalalignment='center', transform=cax.transAxes
                )

                ax.text(
                    x, 0.5, r"$n$-gram"+"\nrank\n"+r"$r$", ha='center',
                    verticalalignment='center', transform=ax.transAxes
                )

                ax.text(
                    x, 0.1, "Less\nTalked\nAbout\n↓", ha='center', fontsize=8,
                    verticalalignment='center', transform=ax.transAxes, color='grey'
                )
                ax.text(
                    x, 0.9, "↑\nMore\nTalked\nAbout", ha='center', fontsize=8,
                    verticalalignment='center', transform=ax.transAxes, color='grey'
                )

            i += 1

        plt.subplots_adjust(top=0.97, right=0.97, hspace=0.5)
        plt.savefig(f'{savepath}.pdf', bbox_inches='tight', pad_inches=.25)
        plt.savefig(f'{savepath}.png', dpi=300, bbox_inches='tight', pad_inches=.25)

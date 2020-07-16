"""
Contagiograms
Copyright (c) 2020 The Computational Story Lab.
Licensed under the MIT License;
"""

import ujson
import numpy as np
import pandas as pd
from pathlib import Path
from datetime import datetime


import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.dates as mdates
import matplotlib.colors as mcolors
import matplotlib.ticker as ticker

from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from bidi import algorithm as bidialg
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

import consts, regexr
from query import Query


import warnings
warnings.simplefilter("ignore")


def plot(
        grams,
        savepath,
        lang_hashtbl=consts.supported_languages,
        nparser=consts.ngrams_parser,
        case_sensitive=True,
        start_date=datetime(2010, 1, 1)
):
    """ Plot a grid of contagiograms

    Args:
        grams: a dict list of n-grams to parse out
        savepath: path to save generated plot
        lang_hashtbl: a list of languages and their corresponding codes in both FastText and Twitter
        nparser: compiled ngram parser
        case_sensitive: a toggle for case_sensitive lookups
        start_date: starting date for the query
    """

    Path(savepath).mkdir(parents=True, exist_ok=True)

    if type(grams) != dict:
        with open(grams, 'r') as data:
            grams = ujson.load(data)

    for key, listt in grams.items():
        ngrams = []
        for i, (w, lang) in enumerate(listt[:12]):
            n = len(regexr.ngrams(w, parser=nparser, n=1))
            print(f"Retrieving {lang_hashtbl.get(lang)}: {n}gram -- '{w}'")

            q = Query(f'{n}grams', lang)

            if case_sensitive:
                d = q.query_timeseries(w, start_time=start_date)
            else:
                d = q.query_insensitive_timeseries(w, start_time=start_date)

            d.index.name = f"{lang_hashtbl.get(lang)}\n'{w}'" \
                if lang_hashtbl.get(lang) is not None else f"All\n'{w}'"

            q = Query('languages', 'languages')
            lang = q.query_languages(lang, start_time=start_date)
            d['lang_count'] = lang['count']
            d['lang_count_no_rt'] = lang['count_no_rt']
            ngrams.append(d)

        plot_contagiograms(
            f'{savepath}/{datetime.date(datetime.now())}_contagiograms_{key}',
            ngrams,
            shading=True,
            fullpage=True if len(ngrams) > 6 else False
        )
        print(f'Saved: {savepath}/{datetime.date(datetime.now())}_contagiograms_{key}')


def plot_contagiograms(savepath, ngrams, shading=True, fullpage=False):
    """ Plot a grid of contagiograms

    Args:
        savepath: path to save plot
        ngrams: a 2D-list of ngrams to plot
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
    rows = (r*size)+r if fullpage else (r*size)+r
    cols = 3 if fullpage else 2
    fig = plt.figure(figsize=(12, size+(2*r+2))) if fullpage else plt.figure(figsize=(8, size+(2*r)))
    gs = fig.add_gridspec(ncols=cols, nrows=rows)
    metric = 'rank'
    labels = 'A B C D E F G H I J K L M N O P Q R S T U V W X Y Z'.split(' ')
    window_size = 30
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    vmin, vmax, vcenter, step = 0, 3, 1, .1
    contagion_color = 'orangered'
    rtcmap = plt.get_cmap('OrRd', 256)
    otcmap = plt.get_cmap('Greys_r', 256)

    cmap = np.vstack((
        otcmap(np.linspace(.4, 1, int(abs(vcenter - vmin)/step))),
        rtcmap(np.linspace(0, 1, int(abs(vcenter - vmax)/step)))
    ))
    cmap = mcolors.ListedColormap(cmap)
    minr, maxr = 1, 10**6

    start_date = ngrams[0].index[0]
    end_date = ngrams[0].index[-1]
    diff = end_date - start_date

    if diff.days < 365:
        date_format = '%m\n%Y'
        major_locator = mdates.MonthLocator(range(1, int(np.ceil(diff.days/30) + 1)))
        minor_locator = mdates.AutoDateLocator()
        contagion_resolution = 'W'

    else:
        date_format = '%Y'
        major_locator = mdates.YearLocator(2)
        minor_locator = mdates.YearLocator()
        contagion_resolution = 'M'

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
            ax.xaxis.set_major_formatter(mdates.DateFormatter(date_format))
            ax.xaxis.set_minor_locator(minor_locator)

            cax.xaxis.set_major_locator(major_locator)
            cax.xaxis.set_major_formatter(mdates.DateFormatter(date_format))
            cax.xaxis.set_minor_locator(minor_locator)

            langax.xaxis.set_major_locator(major_locator)
            langax.xaxis.set_major_formatter(mdates.DateFormatter(date_format))
            langax.xaxis.set_minor_locator(minor_locator)

            df['count'] = df['count'].fillna(0)
            df['count_no_rt'] = df['count_no_rt'].fillna(0)

            df['freq'] = df['freq'].fillna(0)
            df['freq_no_rt'] = df['freq_no_rt'].fillna(0)

            df['rank'] = df['rank'].fillna(maxr)
            df['rank_no_rt'] = df['rank_no_rt'].fillna(maxr)

            alpha = (
                (df['count'] - df['count_no_rt']) / df['count']
            ) / ((df['lang_count'] - df['lang_count_no_rt']) / df['lang_count'])
            alpha = alpha.replace([np.inf, -np.inf, np.nan], 1)

            at = df['count'].resample(contagion_resolution).mean()
            ot = df['count_no_rt'].resample(contagion_resolution).mean()
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
                try:
                    idx = np.where((rt - ot) > 0)[0]
                    if len(idx) > 0:
                        for d in rt[idx].index:
                            cax.axvline(d, color=contagion_color, alpha=.25)

                except IndexError:
                    pass

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
                    df[metric].rolling(window_size, center=True).mean(),
                    color='k',
                    lw=1,
                )

            except ValueError as e:
                print(f'Value error for {df.index.name}: {e}.')
                pass

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
                ticker.LogLocator(base=10.0, subs=(0.2, 0.4, 0.6, 0.8), numticks=30)
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
                    bbox_to_anchor=(1.22, .5),
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
                cbarax.set_ylabel(r'$\alpha$', rotation=0, labelpad=10)

            if c == 0:
                langax.text(
                    -0.22, 0.5, r"$\alpha = \dfrac{p_{\tau}^{(\mathsf{RT})}}{p_{\ell}^{(\mathsf{RT})}}$", ha='center',
                    verticalalignment='center', transform=langax.transAxes
                )

                cax.text(
                    -0.22, 0.5, f"OT/RT\nBalance", ha='center',
                    verticalalignment='center', transform=cax.transAxes
                )

                ax.text(
                    -0.22, 0.5, r"$n$-gram"+"\nrank\n"+r"$r$", ha='center',
                    verticalalignment='center', transform=ax.transAxes
                )

                ax.text(
                    -0.22, 0.1, "Less\nTalked\nAbout\n↓", ha='center', fontsize=8,
                    verticalalignment='center', transform=ax.transAxes, color='grey'
                )
                ax.text(
                    -0.22, 0.9, "↑\nMore\nTalked\nAbout", ha='center', fontsize=8,
                    verticalalignment='center', transform=ax.transAxes, color='grey'
                )

            i += 1

        plt.subplots_adjust(top=0.97, right=0.97, hspace=0.5)
        plt.savefig(f'{savepath}.pdf', bbox_inches='tight', pad_inches=.25)
        plt.savefig(f'{savepath}.png', dpi=300, bbox_inches='tight', pad_inches=.25)


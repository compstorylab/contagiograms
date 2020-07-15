"""
Contagiograms
Copyright (c) 2020 The Computational Story Lab.
Licensed under the MIT License;
"""

import sys
import time
import json
from pathlib import Path
from datetime import datetime

import cli
import utils
import regexr
import consts


def parse_args(args):
    parser = cli.parser()

    # optional subparsers
    subparsers = parser.add_subparsers(help='Arguments for specific action.', dest='dtype')
    subparsers.required = True

    ngrams_parser = subparsers.add_parser(
        'ngrams',
        help='plot a grid of contagiograms: rate of usage timeseries + RT/OT balance + relative amplification heatmap'
    )
    ngrams_parser.add_argument(
        'datapath',
        help='path to an input JSON file',
        default=None,
    )
    ngrams_parser.add_argument(
        'savepath',
        help='path to save figure'
    )

    lang_parser = subparsers.add_parser(
        'langs',
        help='Plot a grid of language contagion diagrams: rate of usage timeseries + RT/OT balance'
    )
    lang_parser.add_argument(
        'targets',
        default=None,
        help='list of languages to use (eg, "en es ja")'
    )

    lang_parser.add_argument(
        'savepath',
        help='path to save figure'
    )

    return parser.parse_args(args)


def main(args=None):
    timeit = time.time()

    if args is None:
        args = sys.argv[1:]

    args = parse_args(args)
    Path(args.savepath).mkdir(parents=True, exist_ok=True)

    if args.dtype == 'ngrams':
        nparser = regexr.get_ngrams_parser(consts.ngrams_parser)

        if args.datapath is None:
            ngrams = consts.contagiograms
        else:
            with open(args.datapath, 'r') as data:
                ngrams = json.load(data)

        utils.contagiograms(
            ngrams,
            savepath=Path(args.savepath),
            lang_hashtbl=consts.supported_languages,
            nparser=nparser,
            case_sensitive=True,
            start_date=datetime(2010, 1, 1)
        )

    elif args.dtype == 'langs':

        if args.targets is None:
            loi = consts.loi
        else:
            loi = args.targets.split(' ')

        utils.lang_contagiograms(
            loi,
            savepath=Path(args.savepath),
            lang_hashtbl=consts.supported_languages,
            start_date=datetime(2010, 1, 1)
        )

    else:
        print('Error: unknown action!')

    print(f'Total time elapsed: {time.time() - timeit:.2f} sec.')


if __name__ == "__main__":
    main()

"""
Contagiograms
Copyright (c) 2020 The Computational Story Lab.
Licensed under the MIT License;
"""

import sys
import time
from datetime import datetime
from pathlib import Path

import cli
import consts
import utils


def parse_args(args):
    parser = cli.parser()

    parser.add_argument(
        "-o", "--output", help="path to save figure", default=Path.cwd(),
    )

    parser.add_argument(
        "-i", "--input", help="path to an input JSON file", default=None,
    )

    parser.add_argument(
        "--flipbook",
        help="a flag to combine contagiograms PDFs into a single flipbook",
        action="store_true",
    )

    parser.add_argument(
        "--t1",
        help="time scale to investigate relative social amplification [eg, M, 2M, 6M, Y]",
        default="1M",
        type=cli.valid_timescale,
    )

    parser.add_argument(
        "--t2",
        help="window size for smoothing the main timeseries [days]",
        default=int(30),
        type=cli.valid_windowsize,
    )

    parser.add_argument(
        "--start_date",
        help="starting date for the query",
        default=datetime(2010, 1, 1),
        type=cli.valid_date,
    )

    return parser.parse_args(args)


def main(args=None):
    timeit = time.time()

    args = parse_args(args)

    utils.plot(
        consts.contagiograms if args.input is None else Path(args.input),
        savepath=Path(args.output),
        lang_hashtbl=consts.supported_languages,
        nparser=consts.ngrams_parser,
        start_date=args.start_date,
        t1=args.t1,
        t2=args.t2,
    )

    if args.flipbook:
        utils.flipbook(
            savepath=Path(args.output), datapath=Path(args.output),
        )

    print(f"Total time elapsed: {time.time() - timeit:.2f} sec.")


if __name__ == "__main__":
    main()

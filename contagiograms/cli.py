"""
Contagiograms
Copyright (c) 2020 The Computational Story Lab.
Licensed under the MIT License;
"""

import argparse
import re
from argparse import ArgumentDefaultsHelpFormatter
from datetime import datetime
from operator import attrgetter
from pathlib import Path


class SortedMenu(ArgumentDefaultsHelpFormatter):
    def add_arguments(self, actions):
        actions = sorted(actions, key=attrgetter("option_strings"))
        super(SortedMenu, self).add_arguments(actions)


def get_parser():
    return argparse.ArgumentParser(
        formatter_class=SortedMenu,
        description="Contagiograms; Copyright (c) 2020 The Computational Story Lab. Licensed under the MIT License.",
    )


def valid_timescale(t):
    try:
        match = re.match("[1-9][M,Y]", t)
        if match:
            return t
        else:
            raise argparse.ArgumentTypeError(f"Timescale format should be [1-9][M,Y]")
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid timescale: '{t}'")


def valid_windowsize(w):
    try:
        w = int(w)
        if w > 0:
            return w
        else:
            raise argparse.ArgumentTypeError("Window size must be a positive number!")
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid window size: '{w}'")


def valid_date(d):
    try:
        return datetime.strptime(d, "%Y-%m-%d")
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid date format: '{d}'")


def parse_args(args):
    parser = get_parser()

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
        type=valid_timescale,
    )

    parser.add_argument(
        "--t2",
        help="window size for smoothing the main timeseries [days]",
        default=int(30),
        type=valid_windowsize,
    )

    parser.add_argument(
        "--start_date",
        help="starting date for the query",
        default=datetime(2010, 1, 1),
        type=valid_date,
    )

    return parser.parse_args(args)

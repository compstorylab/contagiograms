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


class SortedMenu(ArgumentDefaultsHelpFormatter):
    def add_arguments(self, actions):
        actions = sorted(actions, key=attrgetter("option_strings"))
        super(SortedMenu, self).add_arguments(actions)


def parser():
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

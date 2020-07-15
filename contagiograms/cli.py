"""
Contagiograms
Copyright (c) 2020 The Computational Story Lab.
Licensed under the MIT License;
"""

import argparse
from argparse import ArgumentDefaultsHelpFormatter
from operator import attrgetter


class SortedMenu(ArgumentDefaultsHelpFormatter):
    def add_arguments(self, actions):
        actions = sorted(actions, key=attrgetter('option_strings'))
        super(SortedMenu, self).add_arguments(actions)


def parser():
    """ Util function to parse command-line arguments """

    return argparse.ArgumentParser(
        formatter_class=SortedMenu,
        description="Contagiograms; Copyright (c) 2020 The Computational Story Lab. Licensed under the MIT License."
    )


"""
Contagiograms
Copyright (c) 2020 The Computational Story Lab.
Licensed under the MIT License;
"""

import sys
import time
from pathlib import Path
from datetime import datetime

from contagiograms import cli, utils, consts


def parse_args(args):
    parser = cli.parser()

    parser.add_argument(
        '-o', '--output',
        help='path to save figure',
        default=Path.cwd(),
    )

    parser.add_argument(
        '-i', '--input',
        help='path to an input JSON file',
        default=None,
    )

    return parser.parse_args(args)



def main(args=None):
    timeit = time.time()

    if args is None:
        args = sys.argv[1:]

    args = parse_args(args)

    utils.plot(
        consts.contagiograms if args.input is None else Path(args.input),
        savepath=Path(args.output),
        lang_hashtbl=consts.supported_languages,
        nparser=consts.ngrams_parser,
        case_sensitive=True,
        start_date=datetime(2010, 1, 1)
    )

    print(f'Total time elapsed: {time.time() - timeit:.2f} sec.')


if __name__ == "__main__":
    main()

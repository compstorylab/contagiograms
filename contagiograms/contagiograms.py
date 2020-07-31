"""
Contagiograms
Copyright (c) 2020 The Computational Story Lab.
Licensed under the MIT License;
"""

import time
from pathlib import Path

import cli
import consts
import utils


def main(args=None):
    timeit = time.time()

    args = cli.parse_args(args)

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

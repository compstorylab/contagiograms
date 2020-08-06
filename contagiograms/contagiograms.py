
import sys
import logging
import time
from pathlib import Path

try:
    from contagiograms import cli
    from contagiograms import consts
    from contagiograms import utils
except ImportError:
    import cli
    import consts
    import utils


logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


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

    logging.info(f"Total time elapsed: {time.time() - timeit:.2f} sec.")


if __name__ == "__main__":
    main()

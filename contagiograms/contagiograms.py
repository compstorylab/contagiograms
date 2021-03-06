
import sys
from pathlib import Path
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

try:
    sys.path.remove(str(parent))
except ValueError:
    pass

try:
    import importlib.resources as pkg_resources
except ImportError:
    import importlib_resources as pkg_resources

import logging
import time
import ujson
from datetime import datetime
from PyPDF2 import PdfFileMerger, PdfFileReader

from storywrangling import Storywrangler
from storywrangling.regexr import nparser
from contagiograms.cli import parse_args
from contagiograms.utils import plot_contagiograms
from contagiograms.consts import examples

__all__ = ["plot", "flipbook", ]


logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


def flipbook(savepath, datapath):
    """ Combine PDFs into a flipBook
    Args:
        savepath: path to save generated pdf
        datapath: directory containing pdfs to be processed
    """
    pdf = PdfFileMerger()
    datapath = Path(datapath)

    for f in sorted(datapath.rglob("*.pdf")):
        logging.info(f)
        pdf.append(PdfFileReader(str(f), "rb"))

    pdf.write(
        f"{savepath}/{datetime.date(datetime.now())}_flipbook_{datapath.stem}.pdf"
    )
    pdf.close()

    logging.info(
        f"Saved: {savepath}/{datetime.date(datetime.now())}_flipbook_{datapath.stem}.pdf"
    )


def plot(
    grams,
    savepath,
    start_date=datetime(2010, 1, 1),
    t1="1M",
    t2=30,
    day_of_the_week=True
):
    """ Plot a grid of contagiograms

    Args:
        grams: a dict list of n-grams to parse out
        savepath: path to save generated plot
        start_date: starting date for the query
        t1: time scale to investigate relative social amplification [eg, M, 2M, 6M, Y]
        t2: window size for smoothing the main timeseries [days]
        day_of_the_week: a toggle to display r_rel by day of the week
    """

    Path(savepath).mkdir(parents=True, exist_ok=True)

    if type(grams) != dict:
        with open(grams, "r") as data:
            grams = ujson.load(data)

    storywrangler = Storywrangler()

    for key, listt in grams.items():
        ngrams = []
        for i, (w, ll) in enumerate(listt[:12]):

            n = len(nparser(w, parser=storywrangler.parser, n=1))
            d = storywrangler.get_ngram(w, lang=ll, start_time=start_date)
            lang = storywrangler.get_lang(ll, start_time=start_date)

            d["lang_count"] = lang["count"]
            d["lang_count_no_rt"] = lang["count_no_rt"]

            d[f"lang_num_ngrams"] = lang[f"num_{n}grams"]
            d[f"lang_num_ngrams_no_rt"] = lang[f"num_{n}grams_no_rt"]

            d[f"lang_unique_ngrams"] = lang[f"unique_{n}grams"]
            d[f"lang_unique_ngrams_no_rt"] = lang[f"unique_{n}grams_no_rt"]

            d.index.name = (
                f"{storywrangler.supported_languages.get(ll)}\n'{w}'"
                if storywrangler.supported_languages.get(ll) is not None
                else f"All\n'{w}'"
            )

            ngrams.append(d)

        plot_contagiograms(
            f"{savepath}/{datetime.date(datetime.now())}_contagiograms_{key}",
            ngrams,
            t1=t1,
            t2=t2,
            fullpage=True if len(ngrams) > 6 else False,
            day_of_the_week=day_of_the_week,
        )
        logging.info(
            f"Saved: {savepath}/{datetime.date(datetime.now())}_contagiograms_{key}"
        )


def main(args=None):
    timeit = time.time()

    args = parse_args(args)

    plot(
        examples if args.input is None else Path(args.input),
        savepath=Path(args.output),
        start_date=args.start_date,
        t1=args.t1,
        t2=args.t2,
        day_of_the_week=args.day_of_the_week
    )

    if args.flipbook:
        flipbook(
            savepath=Path(args.output),
            datapath=Path(args.output),
        )

    logging.info(f"Total time elapsed: {time.time() - timeit:.2f} sec.")


if __name__ == "__main__":
    main()

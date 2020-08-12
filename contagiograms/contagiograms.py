
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
import pickle
from datetime import datetime
from PyPDF2 import PdfFileMerger, PdfFileReader

import resources
import contagiograms.consts
from contagiograms.query import Query
from contagiograms.regexr import nparser
from contagiograms.cli import parse_args
from contagiograms.utils import plot_contagiograms

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

    for f in datapath.rglob("*.pdf"):
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
):
    """ Plot a grid of contagiograms

    Args:
        grams: a dict list of n-grams to parse out
        savepath: path to save generated plot
        start_date: starting date for the query
        t1: time scale to investigate relative social amplification [eg, M, 2M, 6M, Y]
        t2: window size for smoothing the main timeseries [days]
    """

    Path(savepath).mkdir(parents=True, exist_ok=True)

    if type(grams) != dict:
        with open(grams, "r") as data:
            grams = ujson.load(data)

    parser = pickle.load(pkg_resources.open_binary(resources, 'ngrams.bin'))
    supported_languages = ujson.load(pkg_resources.open_text(resources, 'supported_languages.json'))

    for key, listt in grams.items():
        ngrams = []
        for i, (w, lang) in enumerate(listt[:12]):
            n = len(nparser(w, parser=parser, n=1))
            logging.info(f"Retrieving {supported_languages.get(lang)}: {n}gram -- '{w}'")

            q = Query(f"{n}grams", lang)
            d = q.query_timeseries(w, start_time=start_date)

            d.index.name = (
                f"{supported_languages.get(lang)}\n'{w}'"
                if supported_languages.get(lang) is not None
                else f"All\n'{w}'"
            )

            q = Query("languages", "languages")
            lang = q.query_languages(lang, start_time=start_date)

            d["lang_count"] = lang["count"]
            d["lang_count_no_rt"] = lang["count_no_rt"]

            d[f"lang_num_ngrams"] = lang[f"num_{n}grams"]
            d[f"lang_num_ngrams_no_rt"] = lang[f"num_{n}grams_no_rt"]

            d[f"lang_unique_ngrams"] = lang[f"unique_{n}grams"]
            d[f"lang_unique_ngrams_no_rt"] = lang[f"unique_{n}grams_no_rt"]

            ngrams.append(d)

        plot_contagiograms(
            f"{savepath}/{datetime.date(datetime.now())}_contagiograms_{key}",
            ngrams,
            t1=t1,
            t2=t2,
            shading=True,
            fullpage=True if len(ngrams) > 6 else False,
        )
        logging.info(
            f"Saved: {savepath}/{datetime.date(datetime.now())}_contagiograms_{key}"
        )


def main(args=None):
    timeit = time.time()

    args = parse_args(args)

    plot(
        contagiograms.consts.contagiograms if args.input is None else Path(args.input),
        savepath=Path(args.output),
        start_date=args.start_date,
        t1=args.t1,
        t2=args.t2,
    )

    if args.flipbook:
        flipbook(
            savepath=Path(args.output),
            datapath=Path(args.output),
        )

    logging.info(f"Total time elapsed: {time.time() - timeit:.2f} sec.")


if __name__ == "__main__":
    main()

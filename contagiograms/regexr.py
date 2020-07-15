"""
Contagiograms
Copyright (c) 2020 The Computational Story Lab.
Licensed under the MIT License;
"""

import html
import re
import pickle
from collections import Counter


def html2unicode(code):
    """ Converts HTML entities to unicode ('&amp;' => '&') """
    return html.unescape(code)


def hex2unicode(code):
    """ Converts hex-values to unicode ('1F609' => '😉') """
    code = [r'\U' + x.zfill(8) for x in code.split()]
    code = ''.join(code)
    return bytes(code, 'ascii').decode('unicode-escape')


def remove_whitespaces(text):
    """ Strip out extra whitespaces
    :param text: a string
    :return: cleaned text
    """
    text = re.sub(r'\s\s+', ' ', text)
    text = re.sub(r'\n|\t', ' ', text)
    text = re.sub(u'\u20e3|\ufe0f|\u2800|\u200b|\u200c|\u200d|<200b>|<200c>|<200d>', '', text)
    text = text.strip()
    return html2unicode(text)


def ngram_parser(text, ngram_parser):
    """ Parse out N-grams using a custom regex
    :param: text: a string object
    :param ngram_parser: a compiled regex expression to extract one-grams
    :return a list of 1-grams
    """
    # take care of a few edge cases
    text = re.sub(r'(([\-\.]{2,})|(\'\'))', r' \1 ', text)
    return [x[0] for x in ngram_parser.findall(text) if x[0] != '']


def ngrams(s, parser, n=1):
    """ Concatenate tokens into ngrams
    :param s: a string object
    :param parser: a compiled regex expression to extract one-grams
    :param n: the degree of the ngrams
    :return: a Counter object of n-grams
    """
    tokens = ngram_parser(s, parser)

    if len(tokens) == 0:
        return None
    else:
        ngrams = zip(*[tokens[i:] for i in range(n)])
        return Counter([" ".join(ngram) for ngram in ngrams])


def get_emojis_parser(path):
    """ Load a regular expression that matches emojis
    :param path: path to a (.bin) file
    :return: a compiled regex
    """
    print('Loading emoji parser...')
    with open(path, "rb") as f:
        return pickle.load(f)


def get_ngrams_parser(path):
    """ Load a regular expression that matches ngrams
    :param path: path to a (.bin) file
    :return: a compiled regex
    """
    print('Loading ngrams parser...')
    with open(path, "rb") as f:
        return pickle.load(f)


def is_emoji(string, n_emoji, emoji_pattern):
    """Return True if get_emojis() detects emoji. Also check if number of emoji exceeds threshold, and if there are
    non-emoji characters.
    :param string: string to check for emojis
    :param emoji_pattern: emoji pattern
    :param emoji_bin: compiled regex pattern

    """
    try:
        string = string.replace(' ', '')
        regex_res = emoji_pattern.findall(string)
        return len(regex_res) == n_emoji and not len(emoji_pattern.sub('', string)) > 0
    except (TypeError, AttributeError):
        return False


def get_emojis(text, path):
    """ Parse out emojis from a given string
    :param text: a string
    :param path: path to a compiled emoji regex (emojis.bin) file
    :return: a list of re.Match objects in the given the string
    """
    if type(path) == str:
        eparser = get_ngrams_parser(path)
    else:
        eparser = path
    text = remove_whitespaces(text)
    return [m for m in re.finditer(eparser, text)]


def get_ngrams(text, path, n=1):
    """ Parse out ngrams from a given string
    :param text: a string
    :param path: path to a compiled ngrams regex (ngrams.bin) file
    :param n: degree of ngrams to parse out
    :return: a Counter object of ngrams in the given string
    """
    nparser = get_ngrams_parser(path)
    text = remove_whitespaces(text)
    return ngrams(text, nparser, n)

.. image:: tests/2020-07-16_contagiograms_test4.png
   :width: 1000 px
   :scale: 50 %
   :align: center


Contagiograms 
###############

As part of our `StoryWrangler <https://gitlab.com/compstorylab/storywrangler>`_
project, we present a Python package for visualizing contagiograms.



Installation
**************

You can install the latest verion by cloning the repo and running 
`setup.py <setup.py>`_ script in your terminal


.. code-block:: shell

    git clone https://gitlab.com/compstorylab/contagiograms.git
    python setup.py install 


Alternatively, you can use Anaconda to install our package.

.. code-block:: shell

    conda env create -q -f requirements.yml

This will create a new conda environment (``contagiograms``) with all required dependencies. 


Install Development Version
==============================

.. code-block:: shell

    git clone https://gitlab.com/compstorylab/contagiograms.git
    cd contagiograms
    pip install -e .


Usage
********

Python module
===============

.. code-block:: python

    from datetime import datetime
    from contagiograms import utils as cg

    ngrams = {
        "test2": [
            ["Game of Thrones", "en"], ["The Walking Dead", "en"]
        ],
        "test4": [
            ["Copa Mundial", "es"], ["Pasqua", "it"],
            ["@NASA", "en"], ["klimatet", "sv"]
        ]
    }

    cg.plot(ngrams, 'tests/')

    # or using a JSON file 
    cg.plot(
        'tests/test.json', 
        savepath='tests/',
        case_sensitive=True,
        start_date=datetime(2010, 1, 1)
    )

    # combine PDFs into a single flipbook
    cg.flipbook(savepath='.', datapath='tests/')


Command line interface 
=======================

Navigate to the main ``contagiograms`` directory 
and run `contagiograms.py <tescontagiogramsts/contagiograms.py>`_ 

Optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        path to an input JSON file (default: None)
  -o OUTPUT, --output OUTPUT
                        path to save figure (default: ~/contagiograms)

  --flipbook            a flag to combine contagiograms PDFs into a single flipbook (default: False)
  --start_date START_DATE
                        starting date for the query (default: 2010-01-01)
  --t1 T1               time scale to investigate relative social amplification [eg, M, 2M, 6M, Y] (default: 1M)
  --t2 T2               window size for smoothing the main timeseries [days] (default: 30)



Currently, we have five layouts for contagiograms (rows x columns)
    :Configurations: (1 x 2), (1 x 2), (2 x 2), (3 x 2), (3 x 3), and (4 x 3).

To pass in your own ngrams you need a JSON file strucured with any of the configurations noted above (see `test.json <tests/test.json>`_)

.. code-block:: json

    {
        "test2": [
            ["Game of Thrones", "en"], ["The Walking Dead", "en"]
        ],
        "test4": [
            ["Copa Mundial", "es"], ["Pasqua", "it"],
            ["@NASA", "en"], ["klimatet", "sv"]
        ],
        "test6": [
            ["kevät", "fi"], ["Carnaval", "pt"],
            ["Lionel Messi", "es"], ["#TGIF", "en"],
            ["virus", "fr"], ["Brexit", "de"]
        ],
        "test9": [
            ["❤", "en"], ["Resurrección", "es"], ["Coupe", "fr"],
            ["eleição", "pt"], ["ثورة", "ar"], ["@bts_twt", "ko"],
            ["Flüchtling", "de"], ["San Valentino", "it"], ["карантин", "ru"]
        ],
        "test12": [
            ["Avengers", "en"], ["Skyfall", "en"], ["Black Panther", "en"],
            ["Star Wars", "en"], ["Harry Potter", "en"], ["Jurassic World", "en"],
            ["Interstellar", "en"], ["Dark Knight", "en"], ["Inception", "en"],
            ["Frozen", "en"], ["Furious", "en"], ["Titanic", "en"]
        ]
    }


Try it in your terminal 

.. code-block:: shell

    python contagiograms/contagiograms.py --flipbook -i tests/test.json -o tests/



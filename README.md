![contagiograms](tests/2020-08-06_contagiograms_test4.png)


# Contagiograms 

As part of our [StoryWrangler](https://gitlab.com/compstorylab/storywrangler) project, we present a Python package for visualizing contagiograms.

## Description 

With these expanded time series visualizations, we convey the degree to which an n-gram τ is retweeted both overall and relative to the background level of retweeting for a given language ℓ. We show both rates as retweet rates change strongly over time and variably so across languages.

<img src="tests/2020-08-06_contagiograms_test1.png" alt="contagiograms" style="zoom:50%;" />

Each contagiogram has three panels. The main panel at the bottom charts, as before, the rank time series for a given n-gram. For contagiograms running over a decade, we show rank time series in this main panel with month-scale smoothing (black line), and add a background shading in gray indicating the highest and lowest rank of each week.

The top two panels of each contagiogram capture the raw and relative social amplification for each n-gram.

First, the top panel displays the raw R<sub>τ,t,ℓ</sub> balance, the monthly relative volumes of each n-gram in retweets (RT, orange) and organic tweets (OT, blue):

<div align="center">
    <img src="eq1.svg" alt="Eq1" style="zoom:150%;" />
</div>

When the balance of appearances in retweets outweighs those in organic tweets, R<sub>τ,t,ℓ</sub> > 0.5, we view the n-gram as nominally being amplified, and we add a solid background for emphasis.

Second, in the middle panel of each contagiogram, we display a heatmap of the values of the relative amplification rate for n-gram τ in language ℓ, R<sup>rel</sup><sub>τ,t,ℓ</sub>, over time. Building on from the R<sub>τ,t,ℓ</sub> balance, we define R<sup>rel</sup><sub>τ,t,ℓ</sub> as:

<div align="center">
        <img src="eq2.svg" alt="Eq2" style="zoom:150%;" />
</div>

where the denominator gives the overall fraction of n-grams that are found in retweets on day t for language ℓ. While still averaging at month scales, we now do so based on day of the week. Shades of red indicate that the relative volume of n-gram τ is being socially amplified over the baseline of retweets in language ℓ, R<sup>rel</sup><sub>τ,t,ℓ</sub> > 1, while gray encodes the opposite, R<sup>rel</sup><sub>τ,t,ℓ</sub> < 1.


## Installation

You can install the latest verion by cloning the repo and running [setup.py](setup.py) script in your terminal

```shell 
git clone https://gitlab.com/compstorylab/contagiograms.git
cd contagiograms
python setup.py install 
```


### Install Development Version

```shell
git clone https://gitlab.com/compstorylab/contagiograms.git
cd contagiograms
pip install -e .
```

### Anaconda

This will create a new conda environment (``contagiograms``) with all required dependencies. 

```shell
conda env create -q -f requirements.yml
```

## Usage


### Command line interface 

Navigate to the main ``contagiograms`` directory  and run [contagiograms.py](contagiograms/contagiograms.py)
```
usage: contagiograms.py [-h] [-o OUTPUT] [-i INPUT] [--flipbook] [--t1 T1] [--t2 T2] [--start_date START_DATE]

Optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        path to an input JSON file (default: None)
  -o OUTPUT, --output OUTPUT
                        path to save figure (default: ~/contagiograms)

  --flipbook            a flag to combine contagiograms PDFs into a single flipbook (default: False)
  --start_date START_DATE
                        starting date for the query (default: 2010-01-01)
  --t1 T1               time scale to investigate relative social amplification [eg, 1W, 1M, 2M, 6M, 1Y] (default: 1M)
  --t2 T2               window size for smoothing the main timeseries [days] (default: 30)
```

>
> Currently, we have five *layouts* for contagiograms [**rows x columns**]: (1 x 1), (1 x 2), (2 x 2), (3 x 2), (3 x 3), and (4 x 3).
>


To pass in your own ngrams you need a JSON file strucured with any of the configurations noted above (see [test.json](tests/test.json))

```json
{
    "test1": [
        ["Black Lives Matter", "en"]
    ],
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
```

Try it in your terminal 

```shell
python contagiograms/contagiograms.py --flipbook -i tests/test.json -o tests/
```

### Python module

```python
from datetime import datetime
from contagiograms import utils as cg

ngrams = {
    "test1": [
        ["Black Lives Matter", "en"]
    ],
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
    start_date=datetime(2010, 1, 1),
)

# combine PDFs into a single flipbook
cg.flipbook(savepath='.', datapath='tests/')
```


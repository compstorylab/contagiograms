![contagiograms](tests/2020-07-16_contagiograms_test4.png)

# Contagiograms 
As part of our [StoryWrangler](https://gitlab.com/compstorylab/storywrangler) project,
we present a standalone python package for contagiograms:
An instrument to approximate the daily usage of ngrams along with their popularity on Twitter.


## Installation
Let's start by cloning this repo 
```shell
git clone https://gitlab.com/compstorylab/contagiograms.git
```

You can install all required dependencies by running the [setup.py](setup.py) script in your terminal
```shell
python setup.py install 
```

Alternatively, you can use Anaconda to install our package.
To get started, please run the following command:
```shell
conda env create -q -f requirements.yml
```
This will create a new conda environment (`contagiograms`) with all required dependencies. 


## Usage
### Python module
```python
from contagiograms import utils as contagiograms

ngrams = {
    "test2": [
        ["Game of Thrones", "en"], ["The Walking Dead", "en"]
    ],
    "test4": [
        ["Copa Mundial", "es"], ["Pasqua", "it"],
        ["@NASA", "en"], ["klimatet", "sv"]
    ]
}

contagiograms.plot(ngrams, 'tests/')


# or using a JSON file 
contagiograms.plot('tests/contagiograms.json', 'tests')
```

### Command line interface 
If you used Anaconda, you can activate the new environment by running the following command:
```bash 
conda activate contagiograms
```

Once activated, you can navigate to the main directory and run [contagiograms.py](contagiograms/contagiograms.py)

```shell
usage: contagiograms.py [-h] [-o OUTPUT] [-i INPUT]

Contagiograms; Copyright (c) 2020 The Computational Story Lab. Licensed under the MIT License.

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        path to an input JSON file (default: None)
  -o OUTPUT, --output OUTPUT
                        path to save figure (default: ~/contagiograms)
```

Currently, we have five layouts for contagiograms (rows x columns): 
(1 x 2), (2 x 2), (3 x 2), (3 x 3), (4 x 3). 
To pass in your own ngrams you need a JSON file strucured with any of these configurations 
as shown below [test.json](tests/test.json)
```json
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
```

```shell
python contagiograms/contagiograms.py -i tests/contagiograms.json -o tests/
```


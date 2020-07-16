"""
Contagiograms
Copyright (c) 2020 The Computational Story Lab.
Licensed under the MIT License;
"""

import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    libs = f.read().splitlines()

setuptools.setup(
    name='contagiograms',
    version='1.0.0',
    description='An instrument to approximate the daily usage of ngrams along with their popularity on Twitter.',
    long_description=long_description,
    long_description_content_type="text/x-rst",
    keywords='NLP twitter contagion ngrams',
    url='https://gitlab.com/compstorylab/contagiograms',
    author='Thayer Alshaabi',
    author_email='thayer.alshaabi@uvm.edu',
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    install_requires=libs,
    license='MIT',
    classifiers=[
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Text Processing :: Linguistic',
        'Operating System :: OS Independent',
    ],
)

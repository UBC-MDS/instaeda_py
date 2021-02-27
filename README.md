# InstaEDA 

![](https://github.com/jufu/instaeda/workflows/build/badge.svg) [![codecov](https://codecov.io/gh/jufu/instaeda/branch/main/graph/badge.svg)](https://codecov.io/gh/jufu/instaeda) ![Release](https://github.com/jufu/instaeda/workflows/Release/badge.svg) [![Documentation Status](https://readthedocs.org/projects/instaeda/badge/?version=latest)](https://instaeda.readthedocs.io/en/latest/?badge=latest)

Quick and easy way to clean data and build exploratory data analysis plots.

This idea came up as we have been building data projects for quite some time now in the UBC MDS program. We noticed that there are some repetitive activities that occur when we first explore the data. This project will help you take a given raw data set an conduct some data cleansing and plotting with a minimal amount of code.

The main components of this package are:

- **Data Checking**
  - Plot basic information for input data: Take the input data and declare the title of the plot and a list of configurations to be passed to themes to invisibly return the Altair object with summary metrics including the memory usage, the basic description of the input data such as the distribution of the discrete columns, continuous columns, all missing columns, complete rows and missing observations. 
  
- **Data Cleansing**
  - Custom Imputation of missing values in a data frame using additional techniques, i.e quantiles and randomization by dividing data set into several parts and returns combined imputed data frame.

- **Exploratory Visualization**
  - Numerical Correlation Plot: takes in a data frame, selects the numerical columns and outputs a correlation plot object. User can optionally pass in subset of columns to define which columns to compare.
  - Plot Basic Distribution Plot by datatype: Pass in data frame and based on parameters, will return histograms, bar charts, or other chart types depending on the column's datatype.

There are a myriad of packages that provide similar functionality in the Python ecosystem. A few of the more popular packages include:

- [Pandas Profiling](https://github.com/pandas-profiling/pandas-profiling)
- [DataPrep](https://docs.dataprep.ai/index.html)
- [Autoviz](https://pypi.org/project/autoviz/)
- [ExploriPy](https://pypi.org/project/ExploriPy/)

## Installation

```bash
$ pip install -i https://test.pypi.org/simple/ instaeda
```

## Features

- TODO

## Dependencies

- TODO

## Usage

- TODO

## Documentation

The official documentation is hosted on Read the Docs: https://instaeda.readthedocs.io/en/latest/

## Contributors

We welcome and recognize all contributions. You can see a list of current contributors in the [contributors tab](https://github.com/jufu/instaeda/graphs/contributors).

### Credits

This package was created with Cookiecutter and the UBC-MDS/cookiecutter-ubc-mds project template, modified from the [pyOpenSci/cookiecutter-pyopensci](https://github.com/pyOpenSci/cookiecutter-pyopensci) project template and the [audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage).

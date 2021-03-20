# InstaEDA 

![](https://github.com/UBC-MDS/instaeda_py/workflows/build/badge.svg) [![codecov](https://codecov.io/gh/UBC-MDS/instaeda_py/branch/main/graph/badge.svg)](https://codecov.io/gh/UBC-MDS/instaeda_py) ![Release](https://github.com/UBC-MDS/instaeda_py/workflows/Release/badge.svg) [![Documentation Status](https://readthedocs.org/projects/instaeda/badge/?version=latest)](https://instaeda.readthedocs.io/en/latest/?badge=latest)

Quick and easy way to clean data and build exploratory data analysis plots.

This idea came up as we have been building data projects for quite some time now in the UBC MDS program. We noticed that there are some repetitive activities that occur when we first explore the data. This project will help you take a given raw data set an conduct some data cleansing and plotting with a minimal amount of code.

The main components of this package are:

- **Data Checking**
  - Plot basic information for input data: Take the input data and declare the title of the plot and a list of configurations to be passed to themes to invisibly return the Altair object with summary metrics including the memory usage, the basic description of the input data such as the distribution of the discrete columns, continuous columns, all missing columns, complete rows and missing observations. 
  
- **Data Cleansing**
  - Custom Imputation of missing values in a data frame using additional techniques, i.e random shuffling by dividing data set into several parts and filling each part separately then returns combined imputed data frame.

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


## Dependencies

```bash
python = "^3.8"
pandas = "^1.2.3"
palmerpenguins = "^0.1.4"
altair = "^4.1.0"
numpy = "^1.20.1"
vega-datasets = "^0.9.0"
scikit-learn = "^0.24.1"
```

## Usage

```python
from palmerpenguins import load_penguins
from instaeda import instaeda

penguin_df = load_penguins()

#plot_intro
instaeda.plot_intro(penguin_df)

#plot_corr
instaeda.plot_corr(penguin_df)

#divide_and_fill
instaeda.divide_and_fill(penguin_df)

#plot_basic_distributions
dict_plots = instaeda.plot_basic_distributions(penguin_df)
dict_plots['bill_length_mm']   
dict_plots['species']
```

## Documentation

The official documentation is hosted on Read the Docs: https://instaeda.readthedocs.io/en/latest/

## Contributors

We welcome and recognize all contributions. You can see a list of current contributors at the bottom of [CONTRIBUTING.rst](https://github.com/UBC-MDS/instaeda_py/blob/main/CONTRIBUTING.rst)

### Credits

This package was created with Cookiecutter and the UBC-MDS/cookiecutter-ubc-mds project template, modified from the [pyOpenSci/cookiecutter-pyopensci](https://github.com/pyOpenSci/cookiecutter-pyopensci) project template and the [audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage).

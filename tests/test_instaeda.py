from instaeda import __version__
from instaeda import instaeda
import pytest
from palmerpenguins import load_penguins
import pandas as pd
import altair as alt

def test_version():
    assert __version__ == '0.1.0'

@pytest.fixture
def input_dataframe():    
    penguin_df = load_penguins()
    return penguin_df

def test_input_df(input_dataframe):
    rows_in_df = len(input_dataframe)
    assert rows_in_df == 344

def test_plot_basic_distributions(input_dataframe):
    
    with pytest.raises(KeyError) as exc_info:
        instaeda.plot_basic_distributions(input_dataframe, cols=['invalid column name'])     
    assert 'are in the [columns]' in str(exc_info.value) 
    
    with pytest.raises(KeyError) as exc_info:
        instaeda.plot_basic_distributions(input_dataframe, include='unsupported datatype')     
    assert 'The include parameter must be' in str(exc_info.value)     

    with pytest.raises(TypeError) as exc_info:
        instaeda.plot_basic_distributions(['not', 'a', 'dataframe'])             
    assert 'The df parameter must be a pandas dataframe' in str(exc_info.value)     

    dict_plots = instaeda.plot_basic_distributions(input_dataframe)
    for key in dict_plots.keys():
        assert isinstance(dict_plots[key], alt.Chart)

def test_plot_corr(input_dataframe):

    assert corr_plot.mark == "rect", "resulting mark should be type 'rect'"
    assert corr_plot.encoding.color.field == "corr", "correlation values should be plotted on colour"
    assert corr_plot.encoding.color.type == "quantitative", "correlation column passed should be numeric"
    assert corr_plot.data.shape[1] == 3, "dataframe passed to alt.Chart should have 3 columns"
    assert (corr_plot.encoding.x.field == 'variable_1') & (corr_plot.encoding.y.field == 'variable_2'), 
    "map 'variable_1' to x-axis, 'variable_2' to y-axis"
    assert isinstance(corr_plot, alt.Chart), "output expected altair Chart object"

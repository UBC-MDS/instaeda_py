from instaeda import __version__
from instaeda import instaeda
import pytest
from palmerpenguins import load_penguins
import pandas as pd
import altair as alt
import warnings

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
    assert instaeda.plot_corr(input_dataframe).layer[0].mark == "rect", "resulting mark should be type 'rect'"
    assert instaeda.plot_corr(input_dataframe).layer[0].encoding.color.shorthand == 'corr', "correlation values should be plotted on colour"
    assert instaeda.plot_corr(input_dataframe).layer[1].encoding.text.shorthand == 'corr:Q', "text is correlation column passed, numeric"
    assert instaeda.plot_corr(input_dataframe).layer[0].encoding.color.scale.domain == (-1, 1), "correlation values between -1, 1"
    assert (instaeda.plot_corr(input_dataframe).layer[0].encoding.x.shorthand == 'variable_1') & (instaeda.plot_corr(input_dataframe).layer[0].encoding.y.shorthand == 'variable_2'), "map 'variable_1' to x-axis, 'variable_2' to y-axis"
    assert isinstance(instaeda.plot_corr(input_dataframe), alt.LayerChart), "output expected altair Layer Chart object"

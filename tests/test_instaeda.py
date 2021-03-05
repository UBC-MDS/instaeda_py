from instaeda import __version__
from instaeda import instaeda
import pytest
from palmerpenguins import load_penguins
import pandas as pd
import altair as alt
import numpy as np
from sklearn.impute import SimpleImputer
from pandas._testing import assert_frame_equal

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
        
        
def test_divide_and_fill(input_dataframe):
    not_a_dataframe = [[1, 2], [0.5, 0.9], ["a", "b"]]
    not_na_dataframe = pd.DataFrame({"col_1": [1, 2],
                                    "col_2": [0.9, 0.9],
                                    "col_3": ["a", "b"]})
    na_numerical_dataframe = pd.DataFrame({"col_1": [1, 2],
                                           "col_2": [np.nan, 0.9],
                                           "col_3": ["a", "b"]})
    na_categorical_dataframe = pd.DataFrame({"col_1": [1, 2],
                                           "col_2": [0.9, 0.9],
                                           "col_3": ["a", np.nan]})

    # Tests that the correct error message is displayed if a non-dataframe object is passed
    try:
        instaeda.divide_and_fill(not_a_dataframe)
    except Exception:
        pass
    else: 
        raise Exception("Expected an Exception, but none were raised. Not a dataframe.")
        
    # Test that the output for none NA is same as input
    assert isinstance(instaeda.divide_and_fill(not_na_dataframe), pd.DataFrame)
    assert_frame_equal(instaeda.divide_and_fill(not_na_dataframe), not_na_dataframe, check_dtype = False)
    
    # Test that the output for na numerical column
    assert isinstance(instaeda.divide_and_fill(na_numerical_dataframe), pd.DataFrame)
    assert_frame_equal(instaeda.divide_and_fill(na_numerical_dataframe), not_na_dataframe, check_dtype = False)
    
    # Test that the output for na categorical column
    assert isinstance(instaeda.divide_and_fill(na_categorical_dataframe, cols = ['col_3'], 
                                               strategy = 'constant', fill_value = 'b'), 
                      pd.DataFrame)
    assert_frame_equal(instaeda.divide_and_fill(na_categorical_dataframe, cols = ['col_3'], 
                                               strategy = 'constant', fill_value = 'b'), not_na_dataframe, 
                       check_dtype = False)
    # Test for column types and exist in dataframe
    try:
        instaeda.divide_and_fill(na_numerical_dataframe, cols = ["col_1", "col_3"])
        instaeda.divide_and_fill(na_numerical_dataframe, cols = [])
        instaeda.divide_and_fill(na_numerical_dataframe, cols = ["not a column"])
        
    except Exception:
        pass
    else:
        raise Exception("Expected an Exception, but none were raised. Column types and Existance")
    
    #Test for strategy
    try:
        instaeda.divide_and_fill(na_numerical_dataframe, strategy = "most_f")
    except Exception:
        pass
    else:
        raise Exception("Expected an Exception, but none were raised. Strategy.")
    


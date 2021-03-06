from instaeda import __version__
from instaeda import instaeda
import pytest
from palmerpenguins import load_penguins
import pandas as pd
import altair as alt
import numpy as np
from sklearn.impute import SimpleImputer
from pandas._testing import assert_frame_equal
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
    
    # Test input parameters
    with pytest.raises(KeyError) as exc_info:
        instaeda.plot_basic_distributions(input_dataframe, cols=['invalid column name'])     
    assert 'are in the [columns]' in str(exc_info.value) 
    
    with pytest.raises(KeyError) as exc_info:
        instaeda.plot_basic_distributions(input_dataframe, include='unsupported datatype')     
    assert 'The include parameter must be' in str(exc_info.value)     

    with pytest.raises(TypeError) as exc_info:
        instaeda.plot_basic_distributions(['not', 'a', 'dataframe'])             
    assert 'The df parameter must be a pandas dataframe' in str(exc_info.value)     

    with pytest.warns(UserWarning) as exc_info:
        instaeda.plot_basic_distributions(input_dataframe, vega_theme="unsupported theme")        

    with pytest.warns(UserWarning) as exc_info:
        #This should return an empty dictionary (no plots generated)
        instaeda.plot_basic_distributions(input_dataframe, cols=['sex'], include='number')        


    # Tests the output plots
    dict_plots = instaeda.plot_basic_distributions(input_dataframe)
    for key in dict_plots.keys():
        assert isinstance(dict_plots[key], alt.Chart)
    
    assert dict_plots['bill_length_mm'].mark == 'bar'
    assert dict_plots['sex'].mark == 'bar'

    assert dict_plots['bill_length_mm'].encoding.y['shorthand']=='count()'
    assert dict_plots['sex'].encoding.x['shorthand']=='count()'

    assert len(dict_plots.keys()) == 8
    assert list(dict_plots.keys()) == ['bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g', 'year', 'species', 'island', 'sex']
        
        
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
    



def test_plot_corr(input_dataframe):
    assert instaeda.plot_corr(input_dataframe).layer[0].mark == "rect", "resulting mark should be type 'rect'"
    assert instaeda.plot_corr(input_dataframe).layer[0].encoding.color.shorthand == 'corr', "correlation values should be plotted on colour"
    assert instaeda.plot_corr(input_dataframe).layer[1].encoding.text.shorthand == 'corr:Q', "text is correlation column passed, numeric"
    assert instaeda.plot_corr(input_dataframe).layer[0].encoding.color.scale.domain == (-1, 1), "correlation values between -1, 1"
    assert (instaeda.plot_corr(input_dataframe).layer[0].encoding.x.shorthand == 'variable_1') & (instaeda.plot_corr(input_dataframe).layer[0].encoding.y.shorthand == 'variable_2'), "map 'variable_1' to x-axis, 'variable_2' to y-axis"
    assert isinstance(instaeda.plot_corr(input_dataframe), alt.LayerChart), "output expected altair Layer Chart object"

def test_plot_intro(input_dataframe):

    # Check whether the num of all missing columns is an integer
    sum_missing_columns = input_dataframe.isnull().sum(axis = 0) 
    num_of_all_missing_columns = sum(sum_missing_columns)
    assert isinstance(num_of_all_missing_columns, int)

    # Check whether the num of complete rows is an integer
    sum_missing_rows = input_dataframe.isnull().sum(axis = 1)
    num_complete_rows = input_dataframe.shape[0] - sum(sum_missing_rows)
    assert isinstance(num_complete_rows, int)

    # Check the shape of info dataframe 
    info_df = pd.DataFrame({'rows': input_dataframe.shape[0], 
                            'columns': input_dataframe.shape[1],
                            'numeric_columns': len(list(input_dataframe.select_dtypes(include=[np.number]).columns.values)),
                            'all_missing_columns': num_of_all_missing_columns, 
                            'total_missing_values': input_dataframe.isnull().sum().sum(),
                            'complete_rows': num_complete_rows,
                            'total_observations': input_dataframe.shape[0] * input_dataframe.shape[1],
                            'memory_usage': input_dataframe.memory_usage(deep=True).sum(),
                       }, index = [0])
    info_df_rows = info_df.shape[0]
    info_df_cols = info_df.shape[1]
    assert info_df_rows == 1
    assert info_df_cols == 8

    # Check the shape of plotting dataframe
    plot_df = pd.DataFrame({'Metrics': ['Numeric Columns', 'All Missing Columns', 'Missing Observations', 'Complete Rows'], 
                            'Value': [float(info_df['numeric_columns']/info_df['columns']), 
                                      float(info_df['all_missing_columns']/info_df['columns']),
                                      float(info_df['total_missing_values']/info_df['total_observations']),
                                      float(info_df['complete_rows']/info_df['rows'])],
                            'Dimension': ['column', 'column', 'observation', 'row'], 
                })
    plot_df_rows = plot_df.shape[0]
    plot_df_cols = plot_df.shape[1]
    assert plot_df_rows == 4
    assert plot_df_cols == 3

    # Test the altair object
    plot_title = 'Memory Usage: ' + str(float(info_df['memory_usage'])) + 'kb'
    theme_config='Dimension'
    test_plot = instaeda.plot_intro(input_dataframe) 

    assert test_plot.mark == 'bar', 'the result plot should be a bar plot'
    assert isinstance(test_plot, alt.Chart), "output should be an altair Chart object"

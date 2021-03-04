from instaeda import __version__
from instaeda import instaeda
import pytest
from palmerpenguins import load_penguins
import pandas as pd
import altair

def test_version():
    assert __version__ == '0.1.0'

@pytest.fixture
def input_dataframe():    
    penguin_df = load_penguins()
    return penguin_df

def test_input_df(input_dataframe):
    rows_in_df = len(input_dataframe)
    assert rows_in_df == 344
    
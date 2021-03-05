import numpy as np
import pandas as pd
import altair as alt
import warnings

def plot_intro(df, plot_title="", theme_config=""):
    """Takes a dataframe with configurations and returns an altair object with summary metrics.

    Parameters
    -----------
    df: pd.DataFrame
        Dataframe from which to take columns not limited to numerical columns only
    plot_title : string, optional
        User can specify the plot title
    theme_config : list, optional
        A list of color configurations to be passed to theme

    Returns
    -------
    plot : altair.Chart object
        An altair plot object displaying summary metrics including the memory usage and 
        the basic description of the input data.

    Examples
    -------
    >>> example_df = pd.DataFrame({'animal': ['falcon', 'dog', 'spider', 'fish'],
                                    'num_legs': [2, 4, 8, 0],
                                    'num_wings': [2, 0, 0, 0],
                                    'num_specimen_seen': [10, 2, 1, 8]})
    >>> instaeda_py.plot_intro(example_df)
    """
    pass

def plot_corr(df, cols=None, method="pearson", colour_palette="purpleorange"):
    """Takes a dataframe, subsets numeric columns and returns a correlation plot object.

    Parameters
    -----------
    df: pd.DataFrame
        Dataframe from which to take columns and calculate, plot correlation between columns.
    cols: list, optional
        List of columns to perform correlation on. By default, None (perform on all numeric).
    method : string, optional
        correlation calculation method, one of: {'pearson', 'kendall', 'spearman'}. By default 'pearson'
    colour_palette : string, optional
        one of Altair accepted colour schemes

    Returns
    -------
    plot : altair.Chart object
        Correlation plot object displaying column names and corresponding correlation values.

    Examples
    -------
    >>> example_df = pd.DataFrame({'animal': ['falcon', 'dog', 'spider', 'fish'],
                                    'num_legs': [2, 4, 8, 0],
                                    'num_wings': [2, 0, 0, 0],
                                    'num_specimen_seen': [10, 2, 1, 8]})
    >>> instaeda_py.plot_corr(example_df)
    """
    
    # check user input
    assert method in {'pearson', 'kendall', 'spearman'}, "correlation method not acceptable"
    colour_palette_list = {'blueorange', 'brownbluegreen', 'purplegreen', 'pinkyellowgreen', 'purpleorange', 'redblue', 'redgrey', 'redyellowblue', 'redyellowgreen', 'spectral'}
    if colour_palette not in colour_palette_list:
        warnings.warn("Recommended Altair continuous diverging colour palette")
    
    # calculate 
    if cols == None:
        assert(df.select_dtypes(np.number).shape[1] >= 2), "Dataframe does not have enough numeric columns for comparison"
        df = df.select_dtypes(np.number)
    else:
        assert(df[cols].select_dtypes(np.number).shape[1] >= 2), "Dataframe does not have enough numeric columns for comparison"
        df = df[cols].select_dtypes(np.number)
    corr_df = round(df.corr(method=method),4).stack().reset_index(name='corr').rename(columns={'level_0':'variable_1','level_1':'variable_2'})
    
    # plot base plot
    corr_plot = alt.Chart(corr_df, title='Correlations between variables').mark_rect().encode(
    x = alt.X('variable_1', title=''),
    y = alt.Y('variable_2', title=''),
        color = alt.Color('corr', scale = alt.Scale(scheme=colour_palette, domain=(-1, 1)))
    ).properties(height=400, width=400)
    
    # plot corr values
    text = corr_plot.mark_text().encode(
    text='corr:Q',
    color=alt.value('black')
    )
    
    return corr_plot + text

def divide_and_fill(df, cols=None, missing_values = np.nan, strategy = 'mean', fill_value = None, random = False, parts = 1, verbose = 0):
    """Takes a dataframe, subsets selected columns and divides into parts for imputation of missing values and returns a data frame.

    Parameters
    -----------
    df: pd.DataFrame
        Dataframe from which to take columns and check for missing values.
    cols: list, optional
        List of columns to perform imputation on. By default, None (perform on all numeric columns).
    strategy : string, optional
        imputation strategy, one of: {'mean', 'median', 'constant', 'most_frequent', 'quantile_10', 'quantile_90'}. By default, 'mean'.
    fill_value : string or numerical value, optional
        When strategy == 'constant', full_value is used to replace all occurences of missing_values.
        If left to default, fill_value will be 0 when filling numerical data and 'missing' for strings or object data types.
    random : boolean, optional
        When random == True, shuffles data frame before filling. By default, False.
    parts : integer, optional
        The number of parts to divide rows of data frame into. By default, 1.
    verbose : integer, optional
        Controls the verbosity of the divide and fill. By default, 0.
    

    Returns
    -------
    data frame : pandas.DataFrame object
        Data frame obtained after divide and fill on the corresponding columns. 

    Examples
    -------
    >>> import numpy as np
    >>> from instaeda import divide_and_fill
    >>> example_df = pd.DataFrame({'animal': ['falcon', 'dog', 'spider', 'fish'],
                                    'num_legs': [2, 4, 8, np.nan],
                                    'num_wings': [2, np.nan, 0, 0],
                                    'num_specimen_seen': [10, 2, np.nan, np.nan]})
    >>> divide_and_fill(example_df)
    """
    pass



def plot_basic_distributions(df, cols=None, include=None, vega_theme="ggplot2"):
    """Takes a dataframe and generates plots based on types

    Parameters
    -----------
    df: pd.DataFrame
        Dataframe from which to generate plots for each column from
    cols: list, optional
        List of columns to generate plots for. By default, None (builds charts for all columns).
    include: string, optional
        Select the data types to include. Supported types include "string" and "number". By default, it will return both string and number columns.
    vega_theme : string, optional
        Select the vega.themes for the altair plots. The options include: excel, ggplot2, quartz, vox, fivethirtyeight, dark, latimes, urbaninstitute, and googlecharts. By default, it uses ggplot2.

    Returns
    -------
    dict_plots: dict of altair.Chart objects using the column name as the key
        dictionary of generated altair.Chart objects with the column name as the key

    Examples
    -------
    >>> example_df = pd.DataFrame({'animal': ['falcon', 'dog', 'spider', 'fish'],
                                    'num_legs': [2, 4, 8, 0],
                                    'num_wings': [2, 0, 0, 0],
                                    'num_specimen_seen': [10, 2, 1, 8]})
    >>> instaeda_py.plot_distribution(example_df)
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("The df parameter must be a pandas dataframe")


    dict_plots = {}
    df_data = None

    # Set vega theme
    alt.renderers.enable(embed_options={'theme': vega_theme})

    # First filter:  select columns
    if cols is None:    
        df_data = df
    else:
        df_data = df[cols]    
    
    if include not in (None, 'number', 'string'):
        raise KeyError("The include parameter must be None, 'number' or 'string'")

    # Second filter: select types to include
    if include == 'number' or include is None:
        
        df_data_number = df_data.select_dtypes(include="number")        
        for col in df_data_number.columns.tolist():
            dict_plots[col] = alt.Chart(df_data_number).mark_bar().encode(
                                alt.X(col, bin=alt.Bin(maxbins=50)), y='count()')
    
    if include == 'string' or include is None:

        df_data_string = df_data.select_dtypes(include="object")
        for col in df_data_string.columns.tolist():            
            dict_plots[col] = alt.Chart(df_data_string).mark_bar().encode(
                                    x=alt.X('count()'),
                                    y=alt.Y(col, sort='-x')
                                )
            
    return dict_plots
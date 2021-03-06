import numpy as np
import pandas as pd
import altair as alt
from sklearn.impute import SimpleImputer
import warnings


def plot_intro(df, plot_title='', theme_config='Dimension'):
    """Takes a dataframe with configurations and returns an altair object with summary metrics.

    Parameters
    -----------
    df: pd.DataFrame
        Dataframe from which to take columns not limited to numerical columns only
    plot_title : string, optional
        User can specify the plot title, by default to show the memory usage
    theme_config : list, optional
        A list of color configurations to be passed to theme, by default to use Demension as config

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

    # Check basic information for input data
    sum_missing_columns = df.isnull().sum(axis = 0) 
    num_of_all_missing_columns = sum(sum_missing_columns)

    sum_missing_rows = df.isnull().sum(axis = 1)
    num_complete_rows = df.shape[0] - sum(sum_missing_rows)

    # Create info dataframe
    info_df = pd.DataFrame({'rows': df.shape[0], 
                            'columns': df.shape[1],
                            'numeric_columns': len(list(df.select_dtypes(include=[np.number]).columns.values)),
                            'all_missing_columns': num_of_all_missing_columns, 
                            'total_missing_values': df.isnull().sum().sum(),
                            'complete_rows': num_complete_rows,
                            'total_observations': df.shape[0] * df.shape[1],
                            'memory_usage': df.memory_usage(deep=True).sum(),
                       }, index = [0])
    
    # Create the plotting dataframe   
    plot_df = pd.DataFrame({'Metrics': ['Numeric Columns', 'All Missing Columns', 'Missing Observations', 'Complete Rows'], 
                            'Value': [float(info_df['numeric_columns']/info_df['columns']), 
                                      float(info_df['all_missing_columns']/info_df['columns']),
                                      float(info_df['total_missing_values']/info_df['total_observations']),
                                      float(info_df['complete_rows']/info_df['rows'])],
                            'Dimension': ['column', 'column', 'observation', 'row']
                })

    # Create the plot

    ## Check whether the user specifies a plotting title
    if len(plot_title) == 0:
        plot_title = 'Memory Usage: ' + str(float(info_df['memory_usage'])) + 'kb'
        intro_plot = alt.Chart(plot_df, title=plot_title).mark_bar().encode(
            alt.X('Value', axis=alt.Axis(format='%')),
            alt.Y('Metrics'),
            color=alt.Color(theme_config)) 
        
    else:
        intro_plot = alt.Chart(plot_df, title=plot_title).mark_bar().encode(
            alt.X('Value', axis=alt.Axis(format='%')),
            alt.Y('Metrics'),
            color=alt.Color(theme_config)) 

    return intro_plot

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
    correlation_methods = {'pearson', 'kendall', 'spearman'}
    colour_palette_list = {'blueorange', 'brownbluegreen', 'purplegreen', 'pinkyellowgreen', 'purpleorange', 'redblue', 'redgrey', 'redyellowblue', 'redyellowgreen', 'spectral'}
    numeric_cols = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
    if not isinstance(df, pd.DataFrame):
        raise Exception("must pass in pandas DataFrame")
    if method not in correlation_methods:
        raise Exception("correlation method not acceptable")
    if colour_palette not in colour_palette_list:
        warnings.warn("Recommended Altair continuous diverging colour palette")
    
    # calculate 
    if cols == None:
        if (df.select_dtypes(np.number).shape[1] < 2):
            raise Exception("Dataframe does not have enough numeric columns for comparison")
        df = df.select_dtypes(include = numeric_cols)
    else:
        if (df[cols].select_dtypes(np.number).shape[1] < 2):
            raise Exception("Dataframe does not have enough numeric columns for comparison")
        df = df[cols].select_dtypes(include = numeric_cols)
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

def divide_and_fill(
    dataframe,
    cols=None,
    missing_values=np.nan,
    strategy="mean",
    fill_value=None,
    random=False,
    parts=1,
    verbose=0,
):
    """Takes a dataframe, subsets selected columns and divides into parts for imputation of missing values and returns a data frame.

    Parameters
    -----------
    dataframe: pd.DataFrame
        Dataframe from which to take columns and check for missing values.
    cols: list, optional
        List of columns to perform imputation on. By default, None (perform on all numeric columns).
    missing_values: int, float, str, np.nan or None
        The placeholder for the missing values. All occurences of missing values will be imputed.
    strategy : string, optional
        imputation strategy, one of: {'mean', 'median', 'constant', 'most_frequent'}. By default, 'mean'.
    fill_value : string or numerical value, optional
        When strategy == 'constant', fill_value is used to replace all occurences of missing_values.
        If left to default, fill_value will be 0 when filling numerical data and 'missing' for strings or object data types.
    random : boolean, optional
        When random == True, shuffles data frame before filling. By default, False.
    parts : integer, optional
        The number of parts to divide rows of data frame into. By default, 1.
    verbose : integer, optional
        Controls the verbosity of the divide and fill. By default, 0.


    Returns
    -------
    dataframe : pandas.DataFrame object
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
    filled_df = None
    allowed_strategies = ["mean", "median", "constant", "most_frequent"]

    # Checking inputs
    if verbose:
        print("Checking inputs")

    if not isinstance(dataframe, pd.DataFrame):
        raise Exception("The input data must be of type pandas.DataFrame!")

    if cols == None:
        cols = list(dataframe.select_dtypes(include="number").columns)

    if (
        not isinstance(cols, list)
        or not all(isinstance(x, str) for x in cols)
        or not set(cols).issubset(set(dataframe.columns))
    ):
        raise Exception(
            "The input cols must be a list of strings belong to the column names for input dataframe!"
        )

    if (
        not isinstance(missing_values, int)
        and not isinstance(missing_values, float)
        and not isinstance(missing_values, str)
        and (missing_values is not None)
    ):
        raise Exception(
            "The input missing values must be one of the following: (int, float, str, np.nan, None)"
        )

    if strategy not in allowed_strategies:
        raise ValueError(
            "Can only use these strategies: {0} got strategy = {1}".format(
                allowed_strategies, strategy
            )
        )

    if (
        (fill_value is not None)
        and not isinstance(fill_value, int)
        and not isinstance(fill_value, float)
        and not isinstance(fill_value, str)
    ):
        raise Exception(
            "The input fill values must be one of the following: (int, float, str, None)"
        )

    if not isinstance(random, bool):
        raise Exception("The input random must be True or False")

    if not isinstance(parts, int) or (parts < 1):
        raise ValueError("Can only use positive integer parts.")

    if not isinstance(verbose, int):
        raise ValueError("Can only use integer for verbose.")

    # Constructing filled dataframe skeleton.
    if verbose:
        print("Constructing filled dataframe skeleton.")

    if random:
        filled_df = dataframe.copy().sample(frac=1).reset_index(drop=True)
    else:
        filled_df = dataframe.copy()

    if (set(cols) <= set(dataframe.select_dtypes(include="number").columns)):
        if isinstance(fill_value, str) :
            raise ValueError(
                "For numeric columns, can only use fill values: (int, float, None)"
            )
    elif (set(cols) <= set(dataframe.select_dtypes(exclude="number").columns)):
        if isinstance(fill_value, int) or isinstance(fill_value, float):
            raise ValueError(
                "For non-numeric columns, can only use fill values: (None, str)"
            )
    else:
        raise Exception("All items in list cols must be numeric, or non-numeric.")

    # Filling data frame
    spacing = filled_df.shape[0]/(parts + 1)
    indexing = np.arange(0, filled_df.shape[0] + spacing, spacing, dtype=int)
    for i in range(len(indexing) - 1):
        imputer = SimpleImputer(
            missing_values=missing_values, strategy=strategy, fill_value=fill_value
        )
        filled_df.loc[indexing[i] : indexing[i + 1], cols] = imputer.fit_transform(
            filled_df.loc[indexing[i] : indexing[i + 1], cols]
        )

    if verbose:
        print("Returning data frame.")
    return filled_df



def plot_basic_distributions(df, cols=None, include=None, vega_theme="ggplot2"):
    """Takes a dataframe and generates plots based on types

    Parameters
    -----------
    df: pd.DataFrame
        Dataframe from which to generate plots for each column from
    cols: list, optional
        List of columns to generate plots for. By default, None (builds charts for all columns).
    include: string, optional
        Select the data types to include. Supported values include None, "string" and "number". By default, None - it will return both string and number columns.
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


    if vega_theme not in ('excel','ggplot2','quartz','vox','fivethirtyeight', 'dark', 'latimes', 'urbaninstitute', 'googlecharts'):
        warnings.warn("You have selected a theme that is not one of the default Vega color themes.")
    # Set vega theme
    alt.renderers.enable(embed_options={'theme': vega_theme})

    dict_plots = {}
    df_data = None

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

    if len(dict_plots) == 0:
        warnings.warn("Zero plots were generated. Please ensure you specifiy the correct parameters for cols and include")

    return dict_plots
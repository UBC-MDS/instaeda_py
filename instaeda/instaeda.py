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
    pass

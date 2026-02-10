import pandas as pd

def clean_columns(df):
    """
    Clean and standardize DataFrame column names.
    
    Converts all column names to strings, lowercases them,
    strips whitespace, and replaces spaces with underscores.
    
    Parameters
    ----------
    df : pandas.DataFrame
        Input DataFrame.
    
    Returns
    -------
    pandas.DataFrame
        DataFrame with cleaned column names.
    
    Raises
    ------
    Exception
        If input is not a pandas DataFrame with columns.
    """

    if hasattr(df, 'columns'):
        df.columns = df.columns.astype(str).str.lower().str.strip().str.replace(' ', '_', regex=False)
        return df
    else:
        raise Exception('Expected a pandas DataFrame with columns.')
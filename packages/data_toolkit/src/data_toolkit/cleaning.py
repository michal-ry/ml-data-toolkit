import pandas as pd

def clean_columns(df):
    """
    Clean and standardize DataFrame column names.

    This function converts all column names to strings, lowercases them,
    strips leading and trailing whitespace, and replaces spaces with
    underscores. After cleaning, it validates that column names are unique.

    Parameters
    ----------
    df : pandas.DataFrame
        Input DataFrame whose column names will be cleaned.

    Returns
    -------
    pandas.DataFrame
        A DataFrame with cleaned and standardized column names.

    Raises
    ------
    TypeError
        If the input object does not have a `columns` attribute.
    ValueError
        If duplicate column names are detected after cleaning.

    Examples
    --------
    >>> df = clean_columns(df)
    >>> df.columns
    Index(['name', 'total_score', 'age'], dtype='object')
    """

    if hasattr(df, 'columns'):
        df.columns = df.columns.astype(str).str.lower().str.strip().str.replace(' ', '_', regex=False)
        if not df.columns.is_unique:
            dups = df.columns[df.columns.duplicated()].tolist()
            raise ValueError (f"Duplicate column names detected after cleaning: {dups}.")
        return df
    else:
        raise TypeError('Expected a pandas DataFrame with columns.')
import pandas as pd

def clean_columns(df, deal_dups='raise'):

    """
    Clean and standardize pandas DataFrame column names.

    This function modifies `df.columns` using the following rules:
    - convert column names to strings
    - convert all names to lowercase
    - remove leading and trailing whitespace
    - replace spaces with underscores

    Duplicate names may appear after cleaning
    (e.g. " test" and "test " both become "test").

    You can control how duplicates are handled using `deal_dups`:

    - deal_dups="raise" (default):
    Raise a ValueError if duplicate column names are detected.

    - deal_dups="rename":
    Keep the first occurrence unchanged and rename later duplicates
    by adding numeric suffixes:
        "name", "name" -> "name", "name_1"

    If a suffix already exists, the function will increment the number
    until it finds an available name:
        "name", "name", "name_1" -> "name", "name_2", "name_1"

    Parameters
    ----------
    df : pandas.DataFrame
        Input DataFrame. Must be a pandas DataFrame instance.

    deal_dups : str, default "raise"
        How to handle duplicate column names.
        Allowed values:
            - "raise"
            - "rename"

    Returns
    -------
    pandas.DataFrame
        The same DataFrame with cleaned column names.

    Raises
    ------
    TypeError
        If `df` is not a pandas DataFrame.

    ValueError
        If duplicate column names exist and `deal_dups="raise"`,
        or if `deal_dups` is not one of the allowed values.
    """

    if not isinstance(df, pd.DataFrame):
        got_type = type(df).__name__
        raise TypeError(f'Expected a pandas DataFrame. Got: {got_type}')
    
    df.columns = df.columns.astype(str).str.lower().str.strip().str.replace(' ', '_', regex=False)
    if not df.columns.is_unique:
        dups = df.columns[df.columns.duplicated()].tolist()
        if deal_dups == 'raise':
            raise ValueError (f"Duplicate column names detected after cleaning: {dups}.")
        elif deal_dups == 'rename':
            seen = {}
            new_col = []
            unique_columns = set()
            for col in df.columns:
                if col in seen:
                    seen[col] += 1
                    value = seen[col] - 1
                    new_name = f'{col}_{value}'
                    while new_name in df.columns or new_name in unique_columns:
                        value += 1
                        new_name = f'{col}_{value}'
                    new_col.append(new_name)
                    unique_columns.add(new_name)
                else:
                    seen[col] = 1
                    new_col.append(col)
                    unique_columns.add(col)
            df.columns = new_col
        else:
            raise ValueError ('Wrong input in deal_dups argument.')
        
    return df
        
    
def handle_duplicates(df, action='raise'):
    
    if not isinstance(df, pd.DataFrame):
        got_type = type(df).__name__
        raise TypeError(f'Expected a pandas DataFrame. Got: {got_type}')
    
    duplicates_total = df.duplicated().sum()

    if action == 'raise':
        if duplicates_total:
            raise ValueError(f'Duplicates detected. Total number of duplicates: {duplicates_total}')
        else:
            return df
    
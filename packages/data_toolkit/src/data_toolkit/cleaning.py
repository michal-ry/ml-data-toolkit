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
        
    
def handle_duplicates(df, subset=None, action='raise'):

    """
    Detect, report, or remove duplicate rows in a pandas DataFrame.

    This function checks duplicates in the whole DataFrame or in a selected subset
    of columns. Duplicate detection uses `keep='first'`, which means the first
    occurrence is treated as unique and only later duplicates are counted.

    Parameters
    ----------
    df : pandas.DataFrame
        Input DataFrame to analyze.

    subset : None, str, or list, default None
        Columns used to identify duplicates.

        - None: check duplicates using all columns
        - str: check duplicates using one column
        - list: check duplicates using multiple columns

    action : {'raise', 'report', 'clean'}, default 'raise'
        Action to perform when duplicates are checked.

        - 'raise':
        Raise a ValueError if duplicates are detected.
        If no duplicates are found, nothing is returned.
        - 'report':
        Return a dictionary with duplicate summary information.
        - 'clean':
        Return a new DataFrame with duplicate rows removed, keeping the first
        occurrence.

    Returns
    -------
    None
        Returned when `action='raise'` and no duplicates are found.

    dict
        Returned when `action='report'`. The report contains:
        - 'subset_used': list of columns used for duplicate detection
        - 'total_num': number of duplicate rows excluding first occurrences
        - 'total_pct': percentage of duplicate rows

    pandas.DataFrame
        Returned when `action='clean'`. Contains duplicate rows removed according
        to the selected subset and `keep='first'`.

    Raises
    ------
    TypeError
        If `df` is not a pandas DataFrame.
        If `subset` is not None, str, or list.

    ValueError
        If `action` is not supported.
        If `action='raise'` and duplicates are detected.

    Notes
    -----
    - Duplicate count excludes the first occurrence of each duplicated row or group.
    - The input DataFrame is not modified in place.
    - In report mode, if no duplicates are found, 'total_pct' is set to 0.0.
    """

    SUPPORTED_ACTIONS = ['raise', 'report', 'clean']
    
    if not isinstance(df, pd.DataFrame):
        got_type = type(df).__name__
        raise TypeError(f'Expected a pandas DataFrame. Got: {got_type}')
    
    if action not in SUPPORTED_ACTIONS:
        raise ValueError(f"Action not supported. Supported actions: {SUPPORTED_ACTIONS}")
    
    if subset is not None and not isinstance(subset, (str, list)):
        got_type = type(subset).__name__
        raise TypeError(f'Subset should be None, str or a list. Got: {got_type}')

    if isinstance(subset, str):
        subset = [subset]

    df_mask = df.duplicated(subset=subset, keep='first')
    duplicates_total = df_mask.sum()

    if action == 'raise':
        if duplicates_total:
            raise ValueError(f'Duplicates detected. Total number of duplicates: {duplicates_total}')
        
    elif action == 'report':

        if duplicates_total:
            total_pct = duplicates_total / df.shape[0] * 100

        report = {
            'subset_used': subset if subset is not None else df.columns.to_list(),
            'total_num': duplicates_total,
            'total_pct': round(total_pct, 2) if duplicates_total else 0.0
        }

        return report
    
    else:
        df_clean = df.drop_duplicates(subset=subset, keep='first')
        return df_clean

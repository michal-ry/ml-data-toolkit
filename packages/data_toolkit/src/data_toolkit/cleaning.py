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

    if isinstance(subset, list):
        wrong_col = [col for col in subset if col not in set(df.columns)]
        if wrong_col:
            raise ValueError(f'Column names not in DataFrame: {wrong_col}')

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

def report_nan(df, target=None):

    """
    Generate a report of missing values in a pandas DataFrame.

    This function returns a dictionary summarizing missing values across the DataFrame.
    The report always includes:
    - the total number of missing values in the DataFrame
    - a list of feature columns containing missing values

    If a target column is provided, it is reported separately in a dedicated "target" section
    and excluded from the "columns_with_nan" list.

    For each feature column with missing values, the report includes:
    - total number of missing values
    - percentage of missing values

    If the target column is provided, the target section includes:
    - target column name
    - total number of missing values in the target column
    - percentage of missing values in the target column

    Parameters
    ----------
    df : pandas.DataFrame
        Input DataFrame to analyze.

    target : str, optional
        Name of the target column. Must be a non-empty string and must exist in the DataFrame.
        If provided, the target column is reported separately.

    Returns
    -------
    dict
        A dictionary containing the missing values report.

    Raises
    ------
    TypeError
        If `df` is not a pandas DataFrame.
        If `target` is provided and is not a string.

    ValueError
        If the DataFrame has no rows.
        If `target` is an empty or whitespace-only string.
        If `target` is not found in the DataFrame columns.

    Examples
    --------
    >>> import pandas as pd
    >>> import numpy as np
    >>> df = pd.DataFrame({
    ...     "A": [1, np.nan, 3],
    ...     "B": [1, 2, np.nan],
    ...     "target": [1, 0, np.nan]
    ... })
    >>> report_nan(df, target="target")
    {
        'total_nan': 3,
        'columns_with_nan': ['A', 'B'],
        'target': {
            'column_name': 'target',
            'nan_total': 1,
            'nan_pct': 33.33333333333333
        },
        'A': {
            'nan_total': 1,
            'nan_pct': 33.33333333333333
        },
        'B': {
            'nan_total': 1,
            'nan_pct': 33.33333333333333
        }
    }
    """

    if not isinstance(df, pd.DataFrame):
        got_type = type(df).__name__
        raise TypeError(f'Expected a pandas DataFrame. Got: {got_type}')
    
    if df.shape[0] == 0:
        raise ValueError('DataFrame must contain at least one row.')
    
    if target is not None:

        if not isinstance(target, str):
            got_type = type(target).__name__
            raise TypeError(f'Target must be a string. Got: {got_type}')
        
        if not target.strip():
            raise ValueError('Target column cannot be an empty string.')
        
        if target not in df.columns:
            raise ValueError(f'Target column not in DataFrame.\nAvailable columns: {df.columns.to_list()}')

    total_rows = df.shape[0]
    nan_per_col = df.isnull().sum()
    total_nan = nan_per_col.sum()
    columns_with_nan = nan_per_col.loc[nan_per_col > 0].index.to_list()
    if target is not None and target in columns_with_nan:
        columns_with_nan = [col for col in columns_with_nan if col != target]
    nan_pct = nan_per_col / total_rows * 100

    report = {
            'total_nan': total_nan,
            'columns_with_nan': columns_with_nan,
        }
    
    if target is not None:

        report['target'] = {
            'column_name': target,
            'nan_total': nan_per_col[target],
            'nan_pct': nan_pct[target],
        }
    
    if total_nan:
        for col in columns_with_nan:
            report[col] = {
                'nan_total': nan_per_col[col],
                'nan_pct': nan_pct[col]
                }
                
    return report

def drop_nan_target(df, target):

    """
    Remove rows with missing values in the target column.

    This function is designed for supervised machine learning workflows where
    rows with missing target values should be excluded before model training.

    The function validates the input DataFrame and target column, then returns
    a new DataFrame with all rows containing missing values in the target column
    removed. Missing values in other columns are left unchanged.

    Parameters
    ----------
    df : pandas.DataFrame
        Input DataFrame to clean.

    target : str
        Name of the target column. Must be a non-empty string and must exist
        in the DataFrame.

    Returns
    -------
    pandas.DataFrame
        A new DataFrame with rows containing missing values in the target
        column removed.

    Raises
    ------
    TypeError
        If `df` is not a pandas DataFrame.
        If `target` is not a string.

    ValueError
        If the DataFrame has no rows.
        If `target` is an empty or whitespace-only string.
        If `target` is not found in the DataFrame columns.

    Notes
    -----
    This function is intended specifically for handling missing values in the
    target column. It does not fill missing values and does not modify the
    original DataFrame.

    Examples
    --------
    >>> import pandas as pd
    >>> import numpy as np
    >>> df = pd.DataFrame({
    ...     "feature": [10, 20, 30],
    ...     "target": [1, np.nan, 0]
    ... })
    >>> drop_nan_target(df, target="target")
       feature  target
    0       10     1.0
    2       30     0.0
    """

    if not isinstance(df, pd.DataFrame):
        got_type = type(df).__name__
        raise TypeError(f'Expected a pandas DataFrame. Got: {got_type}')
    
    if df.shape[0] == 0:
        raise ValueError('DataFrame must contain at least one row.')
    
    if not isinstance(target, str):
        got_type = type(target).__name__
        raise TypeError(f'Target must be a string. Got: {got_type}')
    
    if not target.strip():
        raise ValueError('Target column cannot be an empty string.')

    if target not in df.columns:
        raise ValueError(f'Target column not in DataFrame.\nAvailable columns: {df.columns.to_list()}')

    df_clean = df.dropna(subset=[target]).copy()

    return df_clean
import re
import numpy as np
import pandas as pd
import pytest
from data_toolkit.cleaning import drop_nan_target


def test_non_df_input_error():

    data = pd.Series([1, 2, 3, 4])
    got_type = type(data).__name__
    expected_message = f'Expected a pandas DataFrame. Got: {got_type}'

    with pytest.raises(TypeError, match=re.escape(expected_message)):
        drop_nan_target(data, target='A')

def test_empty_df_input_error():

    df = pd.DataFrame(columns=['A', 'B', 'C'])
    expected_message = 'DataFrame must contain at least one row.'

    with pytest.raises(ValueError, match=re.escape(expected_message)):
        drop_nan_target(df, target='A')

def test_target_not_string_error():

    df = pd.DataFrame({
    'A': [1, 2, 3, 4],
    'B': [np.nan, 2, 3, 4],
    'C': [1, np.nan, 3, 4]
})
    
    target = 5
    got_type = type(target).__name__
    expected_message = f'Target must be a string. Got: {got_type}'

    with pytest.raises(TypeError, match=re.escape(expected_message)):
        drop_nan_target(df, target=target)

def test_target_empty_string_error():

    df = pd.DataFrame({
    'A': [1, 2, 3, 4],
    'B': [np.nan, 2, 3, 4],
    'C': [1, np.nan, 3, 4]
})
    
    target = ''
    expected_message = 'Target column cannot be an empty string.'

    with pytest.raises(ValueError, match=re.escape(expected_message)):
        drop_nan_target(df, target=target)

def test_target_whitespace_error():

    df = pd.DataFrame({
    'A': [1, 2, 3, 4],
    'B': [np.nan, 2, 3, 4],
    'C': [1, np.nan, 3, 4]
})
    
    target = ' '
    expected_message = 'Target column cannot be an empty string.'

    with pytest.raises(ValueError, match=re.escape(expected_message)):
        drop_nan_target(df, target=target)

def test_target_not_in_df_error():

    df = pd.DataFrame({
    'A': [1, 2, 3, 4],
    'B': [np.nan, 2, 3, 4],
    'C': [1, np.nan, 3, 4]
})

    target = 'D'
    expected_message = f'Target column not in DataFrame.\nAvailable columns: {df.columns.to_list()}'

    with pytest.raises(ValueError, match=re.escape(expected_message)):
        drop_nan_target(df, target=target)
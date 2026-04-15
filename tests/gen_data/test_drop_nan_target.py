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

def test_target_without_nan():

    df = pd.DataFrame({
    'T': [1, 2, 3, 4],
    'A': [1, 2, 3, 4],
    'B': [1, 2, 3, 4]
})
    
    df_clean = drop_nan_target(df, target='T')

    assert df_clean.equals(df)
    assert df_clean is not df

def test_target_with_nan():

    df = pd.DataFrame({
        'T': [1, 2, np.nan, np.nan],
        'A': [1, 2, 3, 4],
        'B': [1, 2, 3, 4]
})
    
    expected_df = pd.DataFrame({
        'T': [1.0, 2.0],
        'A': [1, 2],
        'B': [1, 2]
    })

    df_clean = drop_nan_target(df, target='T')

    assert df_clean.equals(expected_df)
    assert df_clean is not df

def test_other_columns_with_nan():

    df = pd.DataFrame({
        'T': [1, 2, 3, 4],
        'A': [1, np.nan, 3, 4],
        'B': [1, 2, np.nan, 4]
})
    
    expected_df = pd.DataFrame({
        'T': [1, 2, 3, 4],
        'A': [1.0, np.nan, 3.0, 4.0],
        'B': [1.0, 2.0, np.nan, 4.0]
})
    
    df_clean = drop_nan_target(df, target='T')

    assert df_clean.equals(expected_df)
    assert df_clean is not df

def test_target_all_nan():

    df = pd.DataFrame({
        'T': [np.nan, np.nan, np.nan, np.nan],
        'A': [1, 2, 3, 4],
        'B': [1, 2, 3, 4]
})

    df_clean = drop_nan_target(df, target='T')

    assert df_clean.empty
    assert df_clean.columns.tolist() == ['T', 'A', 'B']
    assert df_clean is not df
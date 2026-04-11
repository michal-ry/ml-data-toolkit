import pandas as pd
import pytest
import numpy as np
from data_toolkit.cleaning import report_nan

def test_no_df_input_error():

    data = [1, 2, 3]

    with pytest.raises(TypeError):
        report_nan(data)

def test_empty_df_error():

    df = pd.DataFrame(columns=['A', 'B', 'C'])

    with pytest.raises(ValueError):
        report_nan(df)

def test_target_not_string_error():

    df = pd.DataFrame({
    "id": [1, 2],
    "value": ["A", "B"]
})
    
    target = 11

    with pytest.raises(TypeError):
        report_nan(df, target=target)

def test_target_whitespace_error():

    df = pd.DataFrame({
    "id": [1, 2],
    "value": ["A", "B"]
})
    
    target = "  "

    with pytest.raises(ValueError):
        report_nan(df, target=target)

def test_target_empty_string_error():

    df = pd.DataFrame({
    "id": [1, 2],
    "value": ["A", "B"]
})
    
    target = ""

    with pytest.raises(ValueError):
        report_nan(df, target=target)

def test_target_not_in_df_error():

    df = pd.DataFrame({
    "id": [1, 2],
    "value": ["A", "B"]
})
    
    target = "name"

    with pytest.raises(ValueError):
        report_nan(df, target=target)

def test_report_is_dictionary():

    df = pd.DataFrame({
    "id": [1, 2, 3],
    "value": ["A", "B", "C"]
})
    
    report = report_nan(df)

    assert isinstance(report, dict)

def test_report_no_target_no_nan():

    df = pd.DataFrame({
    'A': [1, 2, 3, 4],
    'B': [1, 2, 3, 4],
    'C': [1, 2, 3, 4]
})
    
    report = report_nan(df)
    
    report_expected = {
        'total_nan': 0,
        'columns_with_nan': [],
    }

    assert report == report_expected

def test_report_no_target_with_nan():

    df = pd.DataFrame({
    'A': [1, 2, 3, 4],
    'B': [np.nan, 2, 3, 4],
    'C': [1, np.nan, 3, 4]
})

    report = report_nan(df)

    report_expected = {
        'total_nan': 2,
        'columns_with_nan': ['B', 'C'],
        'B': {
            'nan_total': 1,
            'nan_pct': 25.0
        },
        'C': {
            'nan_total': 1,
            'nan_pct': 25.0
        },
    }

    assert report == report_expected

def test_report_with_target_no_nan():

    df = pd.DataFrame({
    'A': [1, 2, 3, 4],
    'B': [1, 2, 3, 4],
    'C': [1, 2, 3, 4]
})
    
    report = report_nan(df, target='A')
    
    report_expected = {
        'total_nan': 0,
        'columns_with_nan': [],
        'target': {
            'column_name': 'A',
            'nan_total': 0,
            'nan_pct': 0.0
        },
    }

    assert report == report_expected

def test_report_with_target_and_nan():

    df = pd.DataFrame({
    'A': [np.nan, 2, 3, 4],
    'B': [np.nan, 2, 3, 4],
    'C': [1, 2, 3, 4]
})
    
    report = report_nan(df, target='A')
    
    report_expected = {
        'total_nan': 2,
        'columns_with_nan': ['B'],
        'target': {
            'column_name': 'A',
            'nan_total': 1,
            'nan_pct': 25.0
        },
        'B': {
            'nan_total': 1,
            'nan_pct': 25.0
        },
    }

    assert report == report_expected
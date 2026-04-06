import pandas as pd
import pytest
from data_toolkit.cleaning import report_nan

def test_no_df_input_error():

    data = [1, 2, 3]

    with pytest.raises(TypeError):
        report_nan(data)

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
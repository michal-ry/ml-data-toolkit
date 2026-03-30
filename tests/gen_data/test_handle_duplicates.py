import pandas as pd
import pytest
from data_toolkit.cleaning import handle_duplicates

def test_no_df_input_error():

    data = [1, 2, 3]

    with pytest.raises(TypeError):
        handle_duplicates(data)

def test_invalid_action_input():

    df = pd.DataFrame({
    "id": [1, 2, 3],
    "value": ["A", "B", "C"]
})
    
    with pytest.raises(ValueError):
        handle_duplicates(df, action='drop')
    
def test_invalid_subset_input():

    df = pd.DataFrame({
    "id": [1, 2, 3],
    "value": ["A", "B", "C"]
})
    
    with pytest.raises(TypeError):
        handle_duplicates(df, subset=('id','value'))

def test_missing_columns_list():

    df = pd.DataFrame({
    "id": [1, 2, 3],
    "value": ["A", "B", "C"]
})
    
    with pytest.raises(ValueError):
        handle_duplicates(df, subset=['id', 'name'])
    
def test_missing_column_string():

    df = pd.DataFrame({
    "id": [1, 2, 3],
    "value": ["A", "B", "C"]
})
    
    with pytest.raises(ValueError):
        handle_duplicates(df, subset='name')  

def test_duplicates_raise_mode_error():

    df = pd.DataFrame({
    "id": [1, 2, 2],
    "value": ["A", "B", "B"]
})
    
    with pytest.raises(ValueError):
        handle_duplicates(df, action='raise')

def test_no_duplicates_raise_mode_none():

    df = pd.DataFrame({
    "id": [1, 2, 3],
    "value": ["A", "B", "C"]
})
    
    df_clean = handle_duplicates(df, action='raise')

    assert df_clean is None

def test_is_dictionary_report_mode():

    df = pd.DataFrame({
    "id": [1, 2, 2],
    "value": ["A", "B", "B"]
})
    
    report = handle_duplicates(df, action='report')

    assert isinstance(report, dict)

def test_duplicates_report_mode():

    df = pd.DataFrame({
    "id": [1, 2, 2],
    "value": ["A", "B", "B"]
})
    
    report = handle_duplicates(df, action='report')
    
    assert report['total_num'] > 0
    assert report['total_pct'] > 0

def test_no_duplicates_report_mode():

    df = pd.DataFrame({
    "id": [1, 2, 3],
    "value": ["A", "B", "C"]
})
    
    report = handle_duplicates(df, action='report')
    
    assert report['total_num'] == 0
    assert report['total_pct'] == 0.0

def test_expected_values_duplicates_report_mode():

    df = pd.DataFrame({
    "id": [1, 2, 3, 1],
    "value": ["A", "B", "C", "A"]
})
    
    report = handle_duplicates(df, action='report')

    assert report['total_num'] == 1
    assert report['total_pct'] == 25.0

def test_string_subset_report_mode():
    
    df = pd.DataFrame({
    "id": [1, 2, 3, 1],
    "value": ["A", "B", "C", "A"]
})
    
    report = handle_duplicates(df, action='report', subset='id')

    assert isinstance(report['subset_used'], list)
    assert report['subset_used'] == ['id']

def test_list_subset_report_mode():

    df = pd.DataFrame({
    "id": [1, 2, 3, 1],
    "value": ["A", "B", "C", "A"]
})

    report = handle_duplicates(df, subset=['id', 'value'], action='report')

    assert isinstance(report['subset_used'], list)
    assert report['subset_used'] == ['id', 'value']

def test_none_subset_report_mode():

    df = pd.DataFrame({
    "id": [1, 2, 3, 1],
    "value": ["A", "B", "C", "A"]
})

    report = handle_duplicates(df, subset=None, action='report')

    assert isinstance(report['subset_used'], list)
    assert report['subset_used'] == df.columns.to_list()

def test_return_clean_df_clean_mode():

    df = pd.DataFrame({
    "id": [1, 2, 3, 1],
    "value": ["A", "B", "C", "A"]
})

    clean_df = handle_duplicates(df, action='clean')
    expected_df = df.drop_duplicates(keep="first")

    assert isinstance(clean_df, pd.DataFrame)
    assert clean_df.shape == expected_df.shape
    assert clean_df.equals(expected_df)

def test_keep_first_clean_mode():

    df = pd.DataFrame({
    "id": [1, 2, 3, 1],
    "value": ["A", "B", "C", "A"]
})
    expected_index = [0, 1, 2]
    clean_df = handle_duplicates(df, action='clean')
    
    assert clean_df.index.to_list() == expected_index

def test_original_df_unchanged_clean_mode():

    df = pd.DataFrame({
    "id": [1, 2, 3, 1],
    "value": ["A", "B", "C", "A"]
})

    df_before = df.copy()
    clean_df = handle_duplicates(df, action='clean')

    assert df.equals(df_before)

def test_no_duplicates_clean_mode():

    df = pd.DataFrame({
    "id": [1, 2, 3],
    "value": ["A", "B", "C"]
})
    
    clean_df = handle_duplicates(df, action='clean')

    assert clean_df.equals(df)

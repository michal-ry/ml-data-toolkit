import pandas as pd
from data_toolkit.cleaning import handle_duplicates

def test_no_df_input_error():

    data = [1, 2, 3]

    try:
        handle_duplicates(data)
    except TypeError:
        pass
    else:
        raise AssertionError('TypeError was not raised for non-DataFrame input')

def test_invalid_action_input():

    df = pd.DataFrame({
    "id": [1, 2, 3],
    "value": ["A", "B", "C"]
})

    try:
        handle_duplicates(df, action='drop')
    except ValueError:
        pass
    else:
        raise AssertionError("ValueError was not raised for invalid action.")
    
def test_invalid_subset_input():

    df = pd.DataFrame({
    "id": [1, 2, 3],
    "value": ["A", "B", "C"]
})
    
    try:
        handle_duplicates(df, subset=('id','value'))
    except TypeError:
        pass
    else:
        raise AssertionError("TypeError was not raised for invalid subset.")

def test_missing_columns_list():

    df = pd.DataFrame({
    "id": [1, 2, 3],
    "value": ["A", "B", "C"]
})
    
    try:
        handle_duplicates(df, subset=['id', 'name'])
    except ValueError:
        pass
    else:
        raise AssertionError("ValueError was not raised for missing column names using list.")
    
def test_missing_column_string():

    df = pd.DataFrame({
    "id": [1, 2, 3],
    "value": ["A", "B", "C"]
})

    try:
        handle_duplicates(df, subset='name')
    except ValueError:
        pass
    else:
        raise AssertionError("ValueError was not raised for missing column name using string.")    

def test_duplicates_raise_mode_error():

    df = pd.DataFrame({
    "id": [1, 2, 2],
    "value": ["A", "B", "B"]
})
    
    try:
        handle_duplicates(df, action='raise')
    except ValueError:
        pass
    else:
        raise AssertionError("ValueError was not raised for duplicated DataFrame.")

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

# Test 1: TypeError - non-DataFrame input
test_no_df_input_error()
# Test 2: ValueError - invalid action input
test_invalid_action_input()
# Test 3: TypeError - invalid subset input
test_invalid_subset_input()
# Test 4: ValueError - missing column using list
test_missing_columns_list()
# Test 5: ValueError - missing column name using sting
test_missing_column_string()
# Test 6: ValueError - duplicated DataFrame
test_duplicates_raise_mode_error()
# Test 7 No Duplicates - raise mode:
test_no_duplicates_raise_mode_none()
# Test 8: Return dictionary - report mode
test_is_dictionary_report_mode()
# Test 9: Duplicates - report mode
test_duplicates_report_mode()
# Test 10: No dupicates - report mode
test_no_duplicates_report_mode()
# Test 11: Expected values in dictionary with duploicates - report mode
test_expected_values_duplicates_report_mode()
# Tet 12: Subset string - report mode
test_string_subset_report_mode()
# Test 13: Subset list - report mode
test_list_subset_report_mode()
# Test 14: Subset None - report mode
test_none_subset_report_mode()
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
# Test 7:
test_no_duplicates_raise_mode_none()
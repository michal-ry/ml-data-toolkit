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
    

def test_dupplicates_error():

    df = pd.DataFrame({
    "id": [1, 2, 2],
    "value": ["A", "B", "B"]
})
    
    try:
        handle_duplicates(df, action='raise')
    except ValueError:
        pass
    else:
        raise AssertionError("ValueError was not raise for duplicated DataFrame.")


# Test 1: TypeError - non-DataFrame input
test_no_df_input_error()
# Test 2: ValueError - duplicated DataFrame
test_dupplicates_error()
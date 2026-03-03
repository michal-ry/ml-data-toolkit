import pandas as pd
from data_toolkit.cleaning import handle_duplicates
import sys
print(sys.path)

def test_no_df_input_error():

    data = [1, 2, 3]

    try:
        handle_duplicates(data)
    except TypeError:
        pass
    else:
        raise AssertionError('TypeError was not raised for non-DataFrame input')
    

# Test 1: TypeError - non-DataFrame input
test_no_df_input_error()
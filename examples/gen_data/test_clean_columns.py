import pandas as pd
from data_toolkit.cleaning import clean_columns 

def report(df):

    column_list = df.columns.to_list()
    nr_of_columns = len(df.columns)
    dups = nr_of_columns - df.columns.nunique()
    
    columns = f'List of columns:\n{column_list}'
    number = f'Number of columns: {nr_of_columns}'
    duplicates = f'Number of duplicates: {dups}'

    return columns, number, duplicates


def test_messy_no_duplicates():

    data = {
    " Name ": ["Alice", "Bob", "Charlie"],
    "AGE": [25, 30, 35],
    "Total Score": [80, 90, 85],
    "City  Name": ["NY", "LA", "SF"],
    123: [1, 2, 3],
    "emailAddress": ["a@mail.com", "b@mail.com", "c@mail.com"],
    "Already_clean": [True, False, True],
    "  multiple   spaces  ": [10, 20, 30]
}
    
    df = pd.DataFrame(data)
    
    print('Preview of dataset before cleaning:')
    print(df.head(3))

    cols_pre, number_pre, dups_pre = report(df)
    
    print('\nReport before cleaning:')
    print(cols_pre)
    print(number_pre)
    print(dups_pre)
    
    df = clean_columns(df)
    print('\nColumn names changed successfully!')

    print('\nPreview of dataset after cleaning:')
    print(df.head(3))

    cols_post, number_post, dups_post = report(df)
    print('\nReport after cleaning:')
    print(cols_post)
    print(number_post)
    print(dups_post)
 
# Test 1: messy names, no duplicates
test_messy_no_duplicates()
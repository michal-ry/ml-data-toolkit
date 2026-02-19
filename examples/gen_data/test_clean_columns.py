import pandas as pd
from data_toolkit.cleaning import clean_columns 

def report(df):

    column_list = df.columns.to_list()
    nr_of_columns = len(df.columns)
    dups = nr_of_columns - df.columns.nunique()
    all_strings = all(isinstance(col, str) for col in df.columns)   
    full_report = f'''\
Columns: {column_list}
Number of columns: {nr_of_columns}
Duplicates: {dups}
All strings: {all_strings}
'''
    
    report_dict = {
        'columns': column_list,
        'columns_nr': nr_of_columns,
        'duplicates': dups,
        'all_strings': all_strings,
        'report_all': full_report
    }

    return report_dict


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

    informations = report(df)
    
    print('\nReport before cleaning:')
    print(informations['report_all'])
    
    df = clean_columns(df)
    print('\nColumn names changed successfully!')

    print('\nPreview of dataset after cleaning:')
    print(df.head(3))

    informations = report(df)
    print('\nReport after cleaning:')
    print(informations['report_all'])
    
 
# Test 1: messy names, no duplicates
test_messy_no_duplicates()
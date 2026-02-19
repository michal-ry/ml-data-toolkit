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
    
    info_pre = report(df)
    
    print('\nReport before cleaning:')
    print(info_pre['report_all'])
    
    df = clean_columns(df)

    info_after = report(df)

    assert info_after['duplicates'] == 0
    assert info_after['all_strings']
    assert info_after['columns_nr'] == info_pre['columns_nr']

    print('\nReport after cleaning:')
    print(info_after['report_all'])
    

# Test 1: messy names, no duplicates
test_messy_no_duplicates()
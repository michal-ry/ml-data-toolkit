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
    
    expected_columns = [
    'name',
    'age',
    'total_score',
    'city__name',
    '123',
    'emailaddress',
    'already_clean',
    'multiple___spaces'
]

    df = pd.DataFrame(data)
    
    info_pre = report(df)
    
    df = clean_columns(df)

    info_after = report(df)

    try:
        assert info_after['duplicates'] == 0
        assert info_after['all_strings']
        assert info_after['columns_nr'] == info_pre['columns_nr']
        assert df.columns.to_list() == expected_columns

    except AssertionError:
        print('Report before cleaning:')
        print(info_pre['report_all'])
        print('\nReport after cleaning:')
        print(info_after['report_all'])
        raise

def test_simple_duplicates_rename():

    data = {
    "Name": ["Alice", "Bob", "Charlie"],
    " name ": ["A", "B", "C"],
    "AGE": [25, 30, 35],
    "City": ["NY", "LA", "SF"]
}
    
    expected_columns = ['name', 'name_1', 'age', 'city']

    df = pd.DataFrame(data)

    info_pre = report(df)
    
    df = clean_columns(df, deal_dups='rename')

    info_after = report(df)

    try:
        assert info_after['duplicates'] == 0
        assert info_after['all_strings']
        assert info_after['columns_nr'] == info_pre['columns_nr']
        assert df.columns.to_list() == expected_columns

    except AssertionError:
        print('Report before cleaning:')
        print(info_pre['report_all'])
        print('\nReport after cleaning:')
        print(info_after['report_all'])
        print(f'Expected column names: {expected_columns}')
        raise

def test_duplicate_collision_rename():
    
    data = {
    "Name": ["Alice", "Bob", "Charlie"],
    " name ": ["A", "B", "C"],
    "name_1": [1, 2, 3],
    "NAME": ["X", "Y", "Z"]
}
    
    expected_columns = ['name', 'name_2', 'name_1', 'name_3']

    df = pd.DataFrame(data)

    info_pre = report(df)
    
    df = clean_columns(df, deal_dups='rename')

    info_after = report(df)

    try:
        assert info_after['duplicates'] == 0
        assert info_after['all_strings']
        assert info_after['columns_nr'] == info_pre['columns_nr']
        assert df.columns.to_list() == expected_columns

    except AssertionError:
        print('Report before cleaning:')
        print(info_pre['report_all'])
        print('\nReport after cleaning:')
        print(info_after['report_all'])
        print(f'Expected column names: {expected_columns}')
        raise

def test_non_string_column_names():

    data = {
    123: [1, 2, 3],
    45.6: [4, 5, 6],
    True: ["a", "b", "c"],
    "Name": ["A", "B", "C"]
}
    
    expected_columns = ["123", "45.6", "true", "name"]
    
    df = pd.DataFrame(data)

    info_pre = report(df)
    
    df = clean_columns(df, deal_dups='rename')

    info_after = report(df)

    try:
        assert info_after['all_strings']
        assert info_after['duplicates'] == 0
        assert info_after['columns_nr'] == info_pre['columns_nr']
        assert df.columns.to_list() == expected_columns

    except AssertionError:
        print('Report before cleaning:')
        print(info_pre['report_all'])
        print('\nReport after cleaning:')
        print(info_after['report_all'])
        raise


# Test 1: messy names, no duplicates
test_messy_no_duplicates()
# Test 2: simple duplicates
test_simple_duplicates_rename()
# Test 3: duplicate with collision
test_duplicate_collision_rename()
# Test 4: numeric, non-string values
test_non_string_column_names()
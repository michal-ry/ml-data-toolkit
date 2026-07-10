import pandas as pd

from data_toolkit.cleaning import handle_duplicates


def report_example():

    '''
    Usage example for the handle_duplicates function with action='report'.
    '''

    df = pd.DataFrame(
        {
            "id": [1, 2, 3, 1, 2],
            "value": ["A", "B", "C", "A", "B"],
        }
    )

    report_without_subset = handle_duplicates(df, action='report')
    report_with_subset = handle_duplicates(df, action='report', subset='id')

    print(f'Report without subset:\n{report_without_subset}')
    print()
    print(f'Report with subset:\n{report_with_subset}')


if __name__ == '__main__':
    report_example()
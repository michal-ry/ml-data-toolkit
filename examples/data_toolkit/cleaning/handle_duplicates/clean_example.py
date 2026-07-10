import pandas as pd

from data_toolkit.cleaning import handle_duplicates


def clean_example():

    '''
    Usage example for the handle_duplicates function with action='clean'.
    '''

    df = pd.DataFrame(
        {
            "id": [1, 2, 3, 1, 2],
            "value": ["A", "B", "C", "A", "B"],
        }
    )

    df_clean_without_subset = handle_duplicates(df, action='clean')
    df_clean_with_subset = handle_duplicates(df, subset='id', action='clean')

    print(f'DataFrame after removing duplicates without subset:\n{df_clean_without_subset}')
    print()
    print(f'DataFrame after removing duplicates with subset:\n{df_clean_with_subset}')


if __name__ == '__main__':
    clean_example()
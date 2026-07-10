import pandas as pd

from data_toolkit.cleaning import handle_duplicates


def raise_example():

    '''
    Usage example for the handle_duplicates function with action='raise'.
    '''

    df = pd.DataFrame(
        {
            "id": [1, 2, 3, 1, 2],
            "value": ["A", "B", "C", "A", "B"]
        }
    )
    
    try:
        handle_duplicates(df, action='raise')
    except ValueError as error:
        print(error)


if __name__ == '__main__':
    raise_example()
import pandas as pd

from data_toolkit.cleaning import clean_columns


def raise_on_duplicates():

    '''
    Usage example for the clean_columns function with deal_dups="raise".
    '''

    df = pd.DataFrame(
        {
        " Customer ID ": ["C001", "C002", "C003"],
        "Total Charges": [120.5, 80.0, 200.75],
        " monthly charges ": [29.99, 19.99, 49.99],
        "Churn": ["No", "Yes", "No"],
        " churn ": ["No", "Yes", "No"],
        }
)
    
    df_clean = df.copy()

    try:
        df_clean = clean_columns(df_clean, deal_dups='raise')
    except ValueError as error:
        print(error)


if __name__ == '__main__':
    raise_on_duplicates()
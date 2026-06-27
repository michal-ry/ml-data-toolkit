import pandas as pd
from data_toolkit.cleaning import clean_columns

def clean_columns_example():

    '''
    Usage example for clean_columns function from cleaning module.
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

    df_clean = clean_columns(df_clean, deal_dups='rename')

    print(f'Column names from original DataFrame:\n{df.columns.tolist()}')
    print()
    print(f'Column names after cleaning:\n{df_clean.columns.tolist()}')

if __name__ == '__main__':
    clean_columns_example()
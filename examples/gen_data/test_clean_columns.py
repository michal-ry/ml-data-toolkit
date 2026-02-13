import pandas as pd
from data_toolkit.cleaning import clean_columns 

# Generated "dirty" dataset: messy column names + mixed values
data = {
    "Name": ["Alice", "Bob", "Charlie", None, "Eve"],
    123: [10, 20, 30, 40, 50],
    "UPPER": ["A", "B", "C", "D", "E"],
    "lower": ["x", "y", "z", "x", "y"],
    "aaBaa": [1.5, 2.5, None, 4.5, 5.5],
    " test": [True, False, True, False, True],
    "test ": [100, 100, 200, 200, 300],
    " test test": ["p", "q", "r", "s", "t"],
}

df = pd.DataFrame(data)

print("Original columns:")
print(list(df.columns))
print("\nOriginal preview:")
print(df.head(3))

df = clean_columns(df)

print("\nColumns after cleaning:")
print(list(df.columns))

print("\nDataFrame after cleaning:")
print(df.head(3))

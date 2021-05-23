import pandas as pd
import numpy as np
import re

def is_not_attr(attr):
    return bool(re.match(r"[a-zA-Z]'", attr))

def calculate_prob(df: pd.DataFrame, attr: str, given=None):

    given_mask = [True for _ in range(df.shape[0])]

    if given is not None:
        for column in given:
            if is_not_attr(column):
                column = column[:-1]
                given_mask = given_mask & (df[column] == False)
            else:
                given_mask = given_mask & (df[column] == True)
                
    filtered_df = df[given_mask]

    if filtered_df.shape[0] == 0:
        return 0.0

    if is_not_attr(attr):
        attr = attr[:-1]
        return filtered_df[filtered_df[attr] == False].shape[0]/filtered_df.shape[0]
    else:
        return filtered_df[filtered_df[attr] == True].shape[0]/filtered_df.shape[0]

def calculate_LS(df: pd.DataFrame, h: str, e: str):
    if is_not_attr(h):
        raise Exception("Hypothesis must not be a not probability.")

    not_h = h + "'"
    P_e_h = calculate_prob(df, e, given=[h])
    P_e_not_h = calculate_prob(df, e, given=[not_h])

    if P_e_not_h == 0.0:
        return 'INF'
    
    return P_e_h/P_e_not_h

def calculate_LN(df: pd.DataFrame, h: str, e: str):
    if is_not_attr(h):
        raise Exception("Hypothesis must not be a not probability.")

    not_h = h + "'"
    not_e = e + "'"
    return calculate_prob(df, not_e, given=[h])/calculate_prob(df, not_e, given=[not_h])

def get_filled_columns(series: pd.Series):
    return [column for column in series.index if not pd.isna(series.loc[column])]

def get_missing_columns(series: pd.Series):
    return [column for column in series.index if pd.isna(series.loc[column])]

df = pd.read_csv("generated_csv.csv")

LN_matrix = pd.DataFrame(index=df.columns, columns=df.columns)

for row in LN_matrix.index:
    for column in LN_matrix.columns:
        LN_matrix.loc[row].loc[column] = calculate_LN(df, row, column)

LS_matrix = pd.DataFrame(index=df.columns, columns=df.columns)

for row in LS_matrix.index:
    for column in LS_matrix.columns:
        LS_matrix.loc[row].loc[column] = calculate_LS(df, row, column)

print("\nLS matrix:")
print(LS_matrix)
print("\nLN matrix:")
print(LN_matrix)

missing_data_df = pd.read_csv("generated_missing_data_csv.csv")

for i, row in missing_data_df.iterrows():
    filled_columns = get_filled_columns(row)
    missing_columns = get_missing_columns(row)
    for attr in missing_columns:
        ratio = 1.0
        for column in filled_columns:
            if row.loc[column] == True:
                ratio = ratio * LS_matrix.loc[attr][column]
            else:
                ratio = ratio * LN_matrix.loc[attr][column]
        
        missing_data_df.iloc[i][attr] = ratio > 1.0

missing_data_df.to_csv("filled_missing_data_csv.csv", index=False)
            
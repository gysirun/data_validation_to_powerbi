import pandas as pd
import numpy as np


# Remove duplicates
def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    return df.drop_duplicates()


# Fix date to one standart
def fix_date_types(df: pd.DataFrame, date_cols: list) -> pd.DataFrame:
    for col in date_cols:
        df[col] = pd.to_datetime(df[col], errors="coerce")
    return df


# fill blank value with mode
def fill_missing_media(df: pd.DataFrame) -> pd.DataFrame:
    if "media" in df.columns:
        df["media"] = df["media"].fillna(df["media"].mode()[0])
    return df


# Also it is better to add more checks, for example, negative values(where it is impossible), outliers...
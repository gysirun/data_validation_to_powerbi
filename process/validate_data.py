import pandas as pd


def validate_unique_key(df: pd.DataFrame, key_cols: list):
    print(f"\n--- Checking unique key: {key_cols} ---")
    dups = df[df.duplicated(key_cols, keep=False)]
    print(f"Completed: found {len(dups)} duplicate rows.")
    return dups


def validate_no_nulls(df: pd.DataFrame, critical_cols: list):
    print(f"\n--- Checking null values in columns: {critical_cols} ---")
    missing = df[df[critical_cols].isna().any(axis=1)]
    print(f"Completed: {len(missing)} rows have missing critical values.")
    return missing


def detect_outliers_zscore(df: pd.DataFrame, column: str, threshold: float = 3.0):
    print(f"\n--- Checking outliers using Z-score for '{column}' ---")
    if df[column].std() == 0:
        print("Skipped: zero standard deviation.")
        return pd.DataFrame()

    z = (df[column] - df[column].mean()) / df[column].std()
    outliers = df[z.abs() > threshold]
    print(f"Completed: detected {len(outliers)} outliers.")
    return outliers



def validate_campaign_mapping(fb_df: pd.DataFrame, map_df: pd.DataFrame):
    print("\n--- Checking campaign_id mapping (FB mapping) ---")
    missing = fb_df[~fb_df["campaign_id"].isin(map_df["campaign_id"])]
    print(f"Completed: {len(missing)} unmapped campaign_id found.")
    return missing


def validate_adset_mapping(map_df: pd.DataFrame, gam_df: pd.DataFrame):
    print("\n--- Checking adset_id mapping (mapping GAM) ---")
    missing = map_df[~map_df["adset_id"].isin(gam_df["adset_id"])]
    print(f"Completed: {len(missing)} unmapped adset_id found.")
    return missing


def validate_date_logic(df: pd.DataFrame):

    print("\n--- Checking date logic (ad_date vs created_date) ---")
    if "created_date" not in df.columns or "date" not in df.columns:
        print("Skipped: required columns missing.")
        return pd.DataFrame()

    invalid = df[df["date"] < df["created_date"]]
    print(f"Completed: found {len(invalid)} rows where ad date < created date.")
    return invalid

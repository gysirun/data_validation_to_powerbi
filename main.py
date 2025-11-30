import pandas as pd
from process.load_data import load_excel_sheets, standardize_columns
from process.clean_data import (remove_duplicates, fix_date_types, fill_missing_media)
from process.validate_data import   (validate_unique_key, validate_no_nulls, detect_outliers_zscore,
                                    validate_campaign_mapping, validate_adset_mapping)
from process.upload_xlsx_sql import load_to_postgres
excel_path = "Dataset - Amo Publishing.xlsx"

sheet_map = {
    "creative": "Creative backlog",
    "facebook": "Facebook Ads data",
    "gam": "Google Ad Manager revenue data",
    "mapping": "Campaigns_Adsets"
}

pwd = "***"
uid = "postgres"
server = "localhost"
port = "5433"
db = "amomama"

conn_string = f'postgresql://{uid}:{pwd}@{server}:{port}/{db}'

def step_load_data():
    data = load_excel_sheets(excel_path, sheet_map)

    for key, df in data.items():
        data[key] = standardize_columns(df)

    return data


def step_clean_data(data):
    creative = remove_duplicates(data["creative"])
    facebook = remove_duplicates(data["facebook"])
    gam = remove_duplicates(data["gam"])
    mapping = remove_duplicates(data["mapping"])

    creative = fix_date_types(creative, ["created_date"])
    facebook = fix_date_types(facebook, ["date"])
    gam = fix_date_types(gam, ["date"])

    creative = fill_missing_media(creative)

    return creative, facebook, gam, mapping


def step_validate_data(creative, facebook, gam, mapping):

    print("Duplicate creative keys:", validate_unique_key(creative, ["author", "type", "media", "version", "articleid"]))
    print("Duplicate campaign_id:", validate_unique_key(facebook, ["campaign_id"]))
    print("Missing values in Facebook data:", validate_no_nulls(facebook, ["campaign_id", "date"]))
    print("Unmapped campaign_id:", validate_campaign_mapping(facebook, mapping))
    print("Unmapped adset_id in GAM:", validate_adset_mapping(mapping, gam))
    print("Spend outliers:", detect_outliers_zscore(facebook, "spend"))


def step_load_raw_to_db(creative, facebook, gam, mapping):
    load_to_postgres(creative, "creative", conn_string)
    load_to_postgres(facebook, "facebook", conn_string)
    load_to_postgres(gam, "gam", conn_string)
    load_to_postgres(mapping, "mapping", conn_string)


if __name__ == "__main__":
    print("Loading data...")
    data = step_load_data()

    print("Cleaning data...")
    creative, facebook, gam, mapping = step_clean_data(data)

    print("Validating data...")
    step_validate_data(creative, facebook, gam, mapping)

    print("The process of data manipulation is ended")
    print("Start the process of loading data to PostgreSQL...")

    step_load_raw_to_db(creative, facebook, gam, mapping)
    print("The data export is finished")

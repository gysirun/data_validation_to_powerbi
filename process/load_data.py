import pandas as pd

# the loading data from sheets
def load_excel_sheets(file_path: str, sheet_map: dict) -> dict:
    print(f"The process of loading of sheet:")

    dfs = {}
    for key, sheet_name in sheet_map.items():
        print(sheet_name)
        dfs[key] = pd.read_excel(file_path, sheet_name=sheet_name)
    
    return dfs

# change names to standart view
def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = (df.columns.str.strip().str.lower().str.replace(" ", "_"))
    return df

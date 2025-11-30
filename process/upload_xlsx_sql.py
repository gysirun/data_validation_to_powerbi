from sqlalchemy import create_engine

def load_to_postgres(df, table_name, conn_string):
    try:
        engine = create_engine(conn_string)
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        print(f"Completed: Table '{table_name}' loaded successfully with {len(df)}")
    except Exception as e:
        print("Data load error:", e)

import duckdb
import pandas as pd

class SessionDB:
    def __init__(self):
        self.con = duckdb.connect(database=':memory:')

    def register_df(self, name: str, df: pd.DataFrame):
        self.con.register(name, df)

    def list_tables(self):
        return [r[0] for r in self.con.execute("SHOW TABLES").fetchall()]

    def sql(self, query: str) -> pd.DataFrame:
        return self.con.execute(query).df()

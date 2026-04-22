def execute_query(self, query):
    import pandas as pd
    return pd.read_sql_query(query, self.conn)
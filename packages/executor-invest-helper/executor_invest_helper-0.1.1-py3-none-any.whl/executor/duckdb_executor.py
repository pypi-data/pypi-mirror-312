import duckdb

class DuckDBManager:
    def __init__(self, db_name=':memory:'):
        """Initialize the DuckDB connection."""
        self.connection = duckdb.connect(database=db_name)

    def insert_data(self, table_name, data):
        """
        Insert a list of dictionaries into a specified DuckDB table.

        Parameters:
        - table_name (str): The name of the table to insert data into.
        - data (list): A list of dictionaries containing the data to insert.
        """
        # Create a DataFrame from the list of dictionaries
        df = duckdb.from_df(data)
        
        # Create the table and insert the data
        self.connection.execute(f"CREATE TABLE IF NOT EXISTS {table_name} AS SELECT * FROM df")
        self.connection.execute(f"INSERT INTO {table_name} SELECT * FROM df")

    def execute_query(self, query):
        """
        Execute an arbitrary SQL query against DuckDB.

        Parameters:
        - query (str): The SQL query to execute.
        
        Returns:
        - result: The result of the query execution.
        """
        result = self.connection.execute(query).fetchall()
        return result

    def close(self):
        """Close the DuckDB connection."""
        self.connection.close()
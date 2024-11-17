from typing import Any, List, Optional, Tuple
import pyodbc
import pandas as pd

class DatabaseManager:
    """
    A class to manage database connections, execute queries, and handle results.
    """
    
    def __init__(self, connection_string: str):
        """
        Initialize DatabaseManager with a connection string.
        
        Parameters:
            connection_string (str): The connection string for the database
        """
        self.connection_string = connection_string
        self.connection = None
        self.results_df = None

    def connect(self) -> bool:
        """
        Establishes a connection to the database.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            self.connection = pyodbc.connect(self.connection_string)
            return True
        except pyodbc.Error as e:
            print(f"Connection error: {e}")
            return False

    def build_sql_query(
        self,
        select_clause: str,
        from_clause: str,
        where_conditions: Optional[List[str]] = None,
        order_by_column: Optional[str] = None,
        allowed_sort_columns: Optional[List[str]] = None
    ) -> str:
        """
        Constructs a SQL query dynamically with modular components.

        Parameters:
            select_clause (str): The SELECT clause of the query
            from_clause (str): The FROM clause of the query, including any joins
            where_conditions (Optional[List[str]]): List of conditions for the WHERE clause
            order_by_column (Optional[str]): Column name for sorting
            allowed_sort_columns (Optional[List[str]]): List of valid columns for sorting

        Returns:
            str: The assembled SQL query
        """
        # Assemble the WHERE clause
        where_clause = ""
        if where_conditions:
            where_clause = "WHERE\n    " + "\n    AND ".join(where_conditions)
        
        # Validate and construct the ORDER BY clause
        order_by_clause = ""
        if order_by_column and allowed_sort_columns and order_by_column in allowed_sort_columns:
            order_by_clause = f"ORDER BY\n    {order_by_column} DESC"
        
        # Combine all components to form the final query
        return f"""
        {select_clause}
        {from_clause}
        {where_clause}
        {order_by_clause}
        """

    def execute_query(
        self,
        sql_query: str,
        parameters: Optional[Tuple[Any, ...]] = None
    ) -> Optional[pd.DataFrame]:
        """
        Executes a SQL query and saves the result into a pandas DataFrame.

        Parameters:
            sql_query (str): The SQL query to execute
            parameters (Optional[Tuple[Any, ...]]): Parameters for the query, if applicable

        Returns:
            Optional[pd.DataFrame]: DataFrame containing query results, or None if query fails
        """
        if not self.connection:
            if not self.connect():
                return None

        try:
            with self.connection.cursor() as cursor:
                if parameters:
                    cursor.execute(sql_query, parameters)
                else:
                    cursor.execute(sql_query)
                
                # Fetch column names and data
                columns = [column[0] for column in cursor.description]
                data = cursor.fetchall()
            
            # Convert to pandas DataFrame and store in instance variable
            self.results_df = pd.DataFrame.from_records(data, columns=columns)
            return self.results_df
        
        except pyodbc.Error as e:
            print(f"Query execution error: {e}")
            return None

    def save_results_to_csv(
        self,
        file_path: str,
        include_index: bool = False,
        encoding: str = "utf-8",
        delimiter: str = ","
    ) -> bool:
        """
        Saves the current results DataFrame to a CSV file.

        Parameters:
            file_path (str): The file path for the output CSV file
            include_index (bool): Whether to include the DataFrame index
            encoding (str): Encoding format for the CSV file
            delimiter (str): Delimiter for the CSV file

        Returns:
            bool: True if save successful, False otherwise
        """
        if self.results_df is None:
            print("No results to save. Execute a query first.")
            return False

        try:
            self.results_df.to_csv(
                file_path,
                index=include_index,
                encoding=encoding,
                sep=delimiter
            )
            print(f"Results successfully saved to '{file_path}'")
            return True
        except Exception as e:
            print(f"Error saving results to CSV: {e}")
            return False

    def close(self) -> None:
        """
        Closes the database connection if it exists.
        """
        if self.connection:
            self.connection.close()
            self.connection = None

    def __enter__(self):
        """
        Enables use of context manager (with statement).
        """
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Ensures connection is closed when exiting context.
        """
        self.close()

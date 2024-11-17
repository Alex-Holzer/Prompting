from typing import Any, List, Optional, Tuple
import pyodbc
import pandas as pd
import getpass

class DatabaseManager:
    """
    A class to manage database connections, execute queries, and handle results.
    """
    
    def __init__(self, connection_string_template: str):
        """
        Initialize DatabaseManager with a connection string template.
        
        Parameters:
            connection_string_template (str): The connection string template for the database,
            which will be formatted with the password obtained from the user.
        """
        self.connection_string_template = connection_string_template
        self.connection = None
        self.results_df = None

    def connect(self) -> bool:
        """
        Establishes a connection to the database.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        # Obtain password from the user
        password = getpass.getpass(prompt='Enter database password: ')
        
        # Format the connection string with the password
        connection_string = self.connection_string_template.format(password=password)
        
        try:
            self.connection = pyodbc.connect(connection_string)
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
        if not self.connect():
            return None

        try:
            cursor = self.connection.cursor()
            try:
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
            finally:
                cursor.close()
        except pyodbc.Error as e:
            print(f"Query execution error: {e}")
            return None
        finally:
            self.close()

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
        if not self.connect():
            raise Exception("Failed to establish database connection.")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Ensures connection is closed when exiting context.
        """
        self.close()



# Define your connection string template with a placeholder for the password
connection_string_template = (
    "DRIVER={{ODBC Driver 17 for SQL Server}};"
    "SERVER=your_server;"
    "DATABASE=your_database;"
    "UID=your_username;"
    "PWD={password}"
)

# Initialize the DatabaseManager with the connection string template
db_manager = DatabaseManager(connection_string_template)

# Build your SQL query
sql_query = db_manager.build_sql_query(
    select_clause="SELECT *",
    from_clause="FROM your_table",
    where_conditions=["column_name = 'value'"],
    order_by_column="column_name",
    allowed_sort_columns=["column_name"]
)

# Execute the query and retrieve the results
results_df = db_manager.execute_query(sql_query)

# Check if results were returned and display them
if results_df is not None:
    print(results_df.head())
else:
    print("Query execution failed.")



with DatabaseManager(connection_string_template) as db_manager:
    sql_query = db_manager.build_sql_query(
        select_clause="SELECT *",
        from_clause="FROM your_table",
        where_conditions=["column_name = 'value'"]
    )
    results_df = db_manager.execute_query(sql_query)

    if results_df is not None:
        print(results_df.head())
    else:
        print("Query execution failed.")

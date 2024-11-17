```python

from typing import List, Optional

def build_sql_query(
    select_clause: str,
    from_clause: str,
    where_conditions: Optional[List[str]] = None,
    order_by_column: Optional[str] = None,
    allowed_sort_columns: Optional[List[str]] = None
) -> str:
    """
    Constructs a SQL query dynamically with modular components.

    Parameters:
        select_clause (str): The SELECT clause of the query.
        from_clause (str): The FROM clause of the query, including any joins.
        where_conditions (Optional[List[str]]): List of conditions for the WHERE clause. Defaults to None.
        order_by_column (Optional[str]): Column name for sorting. Defaults to None.
        allowed_sort_columns (Optional[List[str]]): List of valid columns for sorting. Defaults to None.

    Returns:
        str: The assembled SQL query.
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



# Example SQL query components
select_clause = """
SELECT
    c.customer_id,
    c.customer_name,
    o.order_id,
    o.total_amount
"""

from_clause = """
FROM
    customers c
INNER JOIN
    orders o ON c.customer_id = o.customer_id
"""

where_conditions = [
    "o.order_date >= ?",
    "o.order_date <= ?",
    "c.region = ?"
]

allowed_sort_columns = ["customer_name", "order_date", "total_amount"]
sort_column = "total_amount"

# Build the SQL query
sql_query = build_sql_query(
    select_clause=select_clause,
    from_clause=from_clause,
    where_conditions=where_conditions,
    order_by_column=sort_column,
    allowed_sort_columns=allowed_sort_columns
)

print(sql_query)



from typing import Any, List, Optional, Tuple
import pyodbc
import pandas as pd


def execute_query(
    connection: pyodbc.Connection,
    sql_query: str,
    parameters: Optional[Tuple[Any, ...]] = None
) -> pd.DataFrame:
    """
    Executes a SQL query, saves the result into a pandas DataFrame, and closes the connection.

    Parameters:
        connection (pyodbc.Connection): The database connection object.
        sql_query (str): The SQL query to execute.
        parameters (Optional[Tuple[Any, ...]]): Parameters for the query, if applicable. Defaults to None.

    Returns:
        pd.DataFrame: A DataFrame containing the query results.
    """
    try:
        # Execute query and fetch results
        with connection.cursor() as cursor:
            if parameters:
                cursor.execute(sql_query, parameters)
            else:
                cursor.execute(sql_query)
            
            # Fetch column names
            columns = [column[0] for column in cursor.description]
            # Fetch all data
            data = cursor.fetchall()
        
        # Convert to pandas DataFrame
        df = pd.DataFrame.from_records(data, columns=columns)
        return df
    
    except pyodbc.Error as e:
        print(f"An error occurred while executing the query: {e}")
        return pd.DataFrame()
    
    finally:
        # Ensure the connection is closed
        connection.close()


import pyodbc

# Example SQL components
select_clause = """
SELECT
    c.customer_id,
    c.customer_name,
    o.order_id,
    o.total_amount
"""

from_clause = """
FROM
    customers c
INNER JOIN
    orders o ON c.customer_id = o.customer_id
"""

where_conditions = [
    "o.order_date BETWEEN ? AND ?",
    "c.region = ?"
]

allowed_sort_columns = ["customer_name", "order_date", "total_amount"]
sort_column = "total_amount"

# Build SQL query
sql_query = build_sql_query(
    select_clause=select_clause,
    from_clause=from_clause,
    where_conditions=where_conditions,
    order_by_column=sort_column,
    allowed_sort_columns=allowed_sort_columns
)

# Example connection (replace with actual credentials)
conn = pyodbc.connect("DSN=my_database;UID=user;PWD=password")

# Query parameters
parameters = ('2023-01-01', '2023-12-31', 'North')

# Execute the query and save results to a DataFrame
results_df = execute_query(conn, sql_query, parameters)

# Display the DataFrame
print(results_df)



import pandas as pd

def save_dataframe_to_csv(
    dataframe: pd.DataFrame,
    file_path: str,
    include_index: bool = False,
    encoding: str = "utf-8",
    delimiter: str = ","
) -> None:
    """
    Saves a pandas DataFrame to a CSV file.

    Parameters:
        dataframe (pd.DataFrame): The DataFrame to save.
        file_path (str): The file path for the output CSV file.
        include_index (bool): Whether to include the DataFrame index in the CSV file. Defaults to False.
        encoding (str): Encoding format for the CSV file. Defaults to "utf-8".
        delimiter (str): Delimiter for the CSV file. Defaults to ",".

    Returns:
        None
    """
    try:
        dataframe.to_csv(file_path, index=include_index, encoding=encoding, sep=delimiter)
        print(f"DataFrame successfully saved to '{file_path}'")
    except Exception as e:
        print(f"An error occurred while saving the DataFrame to CSV: {e}")



```

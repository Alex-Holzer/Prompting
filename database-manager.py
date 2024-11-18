import getpass
import logging
from typing import Any, Optional, Tuple

import pandas as pd
import pyodbc


class DatabaseConnectionError(Exception):
    """Custom exception for database connection errors."""


class DatabaseQueryError(Exception):
    """Custom exception for database query execution errors."""


class DatabaseManager:
    """
    A class to manage database connections, execute queries, and handle results.
    """

    def __init__(
        self,
        connection_string_template: str,
        timeout: int = 30,
    ):
        """
        Initialize DatabaseManager with a connection string template.

        Parameters:
            connection_string_template (str): The connection string template for the database,
                                              which will be formatted with the user's password.
            timeout (int): The timeout value in seconds for the database connection.
        """
        self.connection_string_template = connection_string_template
        self.timeout = timeout
        self.results_df: Optional[pd.DataFrame] = None
        self.logger = logging.getLogger(__name__)
        self.password = self._get_password()
        self._configure_logging()
        self.has_executed = False  # Flag to ensure only one query is executed per instance

    def _get_password(self) -> str:
        """
        Securely obtains the password from the user.

        Returns:
            str: The password entered by the user.
        """
        return getpass.getpass(prompt='Enter database password: ')

    def _configure_logging(self) -> None:
        """
        Configures the logging settings for the class.
        """
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s %(levelname)s [%(name)s]: %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

        # Set logging level to WARNING to suppress INFO messages
        self.logger.setLevel(logging.WARNING)

    def _connect(self) -> pyodbc.Connection:
        """
        Establishes a connection to the database.

        Returns:
            pyodbc.Connection: The established database connection.

        Raises:
            DatabaseConnectionError: If the connection fails.
        """
        connection_string = self.connection_string_template.format(
            password=self.password
        )

        try:
            connection = pyodbc.connect(
                connection_string,
                timeout=self.timeout,
            )
            self.logger.info("Database connection established.")
            return connection
        except pyodbc.Error as e:
            self.logger.error(f"Failed to connect to the database. Error: {e}")
            raise DatabaseConnectionError("Failed to connect to the database.") from e

    def build_sql_query(self, query_template: str, **kwargs) -> str:
        """
        Builds an SQL query using an f-string template and provided keyword arguments.

        Parameters:
            query_template (str): The SQL query template as an f-string.
            **kwargs: Keyword arguments to be substituted into the query.

        Returns:
            str: The formatted SQL query.
        """
        try:
            query = query_template.format(**kwargs)
            self.logger.debug(f"Built SQL query: {query}")
            return query.strip()
        except KeyError as e:
            self.logger.error(f"Missing query parameter: {e}")
            raise ValueError(f"Missing query parameter: {e}") from e
        except Exception as e:
            self.logger.error(f"Error building SQL query: {e}")
            raise ValueError(f"Error building SQL query: {e}") from e

    def execute_query(
        self,
        sql_query: str,
        parameters: Optional[Tuple[Any, ...]] = None,
    ) -> Optional[pd.DataFrame]:
        """
        Executes a SQL query and returns the result as a pandas DataFrame.

        Parameters:
            sql_query (str): The SQL query to execute.
            parameters (Optional[Tuple[Any, ...]]): Parameters for the query, if applicable.

        Returns:
            Optional[pd.DataFrame]: DataFrame containing query results, or None if an error occurs.

        Raises:
            DatabaseQueryError: If the query execution fails.
            RuntimeError: If the query has already been executed.
        """
        if self.has_executed:
            raise RuntimeError("This instance has already executed a query. Please create a new instance to execute another query.")

        connection = self._connect()

        try:
            cursor = connection.cursor()
            try:
                self.logger.info(f"Executing query: {sql_query}")
                cursor.execute(sql_query, parameters or ())
                self.logger.info("Query executed successfully.")

                # Fetch results
                columns = [column[0] for column in cursor.description]
                data = cursor.fetchall()
                self.results_df = pd.DataFrame.from_records(data, columns=columns)
                self.logger.debug("Fetched query results into DataFrame.")
                self.has_executed = True  # Mark that the query has been executed
                return self.results_df
            finally:
                cursor.close()
                self.logger.info("Cursor closed.")
        except pyodbc.Error as e:
            self.logger.error(f"Failed to execute the query. Error: {e}")
            raise DatabaseQueryError("Failed to execute the query.") from e
        finally:
            connection.close()
            self.logger.info("Database connection closed.")

    def __enter__(self) -> 'DatabaseManager':
        """
        Enables use of context manager (with statement).

        Returns:
            DatabaseManager: The current instance.
        """
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """
        Context manager exit method.
        """
        pass  # No persistent connection to close here


import logging

# Configure root logger
logging.basicConfig(level=logging.WARNING)

# Define your connection string template with double curly braces around the driver name
connection_string_template = (
    "DRIVER={{IBM DB2 ODBC DRIVER}};"
    "HOSTNAME=your_hostname;"
    "PORT=your_port;"
    "DATABASE=your_database;"
    "PROTOCOL=TCPIP;"
    "UID=your_username;"
    "PWD={password};"
)

# Initialize the DatabaseManager
db_manager = DatabaseManager(connection_string_template)

# Define variables for the query
table_name = 'your_table'
limit = 10
column_name = 'your_column'
value = 'some_value'

# Build your SQL query using f-string formatting
sql_query_template = "SELECT * FROM {table_name} WHERE {column_name} = '{value}' FETCH FIRST {limit} ROWS ONLY"

# Build the SQL query
sql_query = db_manager.build_sql_query(
    sql_query_template,
    table_name=table_name,
    column_name=column_name,
    value=value,
    limit=limit
)

# Execute the query and retrieve the results
try:
    results_df = db_manager.execute_query(sql_query)
    if results_df is not None:
        print(results_df.head())
except (DatabaseConnectionError, DatabaseQueryError, RuntimeError, ValueError) as e:
    print(f"An error occurred: {e}")

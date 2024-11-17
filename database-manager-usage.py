# Import the DatabaseManager class
from database_manager import DatabaseManager

# Example 1: Basic Usage with Context Manager
def example_basic_query():
    """
    Basic example showing how to query customer orders using context manager.
    """
    connection_string = "Driver={SQL Server};Server=myserver;Database=mydatabase;UID=myuser;PWD=mypassword"
    
    with DatabaseManager(connection_string) as db:
        # Define query components
        select_clause = """
        SELECT 
            customer_id,
            customer_name,
            COUNT(order_id) as total_orders,
            SUM(order_amount) as total_amount
        """
        
        from_clause = """
        FROM customers c
        LEFT JOIN orders o ON c.customer_id = o.customer_id
        """
        
        where_conditions = [
            "order_date >= ?",
            "order_amount > ?"
        ]
        
        # Build and execute query
        sql_query = db.build_sql_query(
            select_clause=select_clause,
            from_clause=from_clause,
            where_conditions=where_conditions,
            order_by_column="total_amount",
            allowed_sort_columns=["total_amount", "total_orders"]
        )
        
        # Execute with parameters
        results = db.execute_query(sql_query, ('2024-01-01', 1000))
        
        # Save to CSV if results exist
        if results is not None:
            db.save_results_to_csv('customer_orders_summary.csv')


# Example 2: Multiple Queries in One Session
def example_multiple_queries():
    """
    Example showing how to execute multiple queries in one session.
    """
    connection_string = "Driver={SQL Server};Server=myserver;Database=mydatabase;UID=myuser;PWD=mypassword"
    
    db = DatabaseManager(connection_string)
    try:
        # Connect explicitly
        if db.connect():
            # First query: Get top customers
            top_customers_query = db.build_sql_query(
                select_clause="SELECT customer_id, customer_name, total_purchases",
                from_clause="FROM customer_summary",
                where_conditions=["total_purchases > ?"],
                order_by_column="total_purchases",
                allowed_sort_columns=["total_purchases"]
            )
            top_customers = db.execute_query(top_customers_query, (10000,))
            
            if top_customers is not None:
                db.save_results_to_csv('top_customers.csv')
            
            # Second query: Get their recent orders
            recent_orders_query = db.build_sql_query(
                select_clause="SELECT order_id, order_date, order_amount",
                from_clause="FROM orders",
                where_conditions=[
                    "customer_id IN (SELECT customer_id FROM customer_summary WHERE total_purchases > ?)",
                    "order_date >= ?"
                ]
            )
            recent_orders = db.execute_query(recent_orders_query, (10000, '2024-01-01'))
            
            if recent_orders is not None:
                db.save_results_to_csv('recent_orders.csv')
    
    finally:
        # Always close the connection
        db.close()


# Example 3: Complex Query with Multiple Joins
def example_complex_query():
    """
    Example of a more complex query with multiple joins and conditions.
    """
    connection_string = "Driver={SQL Server};Server=myserver;Database=mydatabase;UID=myuser;PWD=mypassword"
    
    with DatabaseManager(connection_string) as db:
        select_clause = """
        SELECT 
            c.customer_id,
            c.customer_name,
            p.product_name,
            cat.category_name,
            COUNT(o.order_id) as order_count,
            SUM(oi.quantity) as total_quantity,
            SUM(oi.quantity * oi.unit_price) as total_amount
        """
        
        from_clause = """
        FROM customers c
        INNER JOIN orders o ON c.customer_id = o.customer_id
        INNER JOIN order_items oi ON o.order_id = oi.order_id
        INNER JOIN products p ON oi.product_id = p.product_id
        INNER JOIN categories cat ON p.category_id = cat.category_id
        """
        
        where_conditions = [
            "o.order_date BETWEEN ? AND ?",
            "c.country = ?",
            "oi.unit_price > ?"
        ]
        
        # Group by clause could be added to the select_clause
        select_clause += """
        GROUP BY
            c.customer_id,
            c.customer_name,
            p.product_name,
            cat.category_name
        """
        
        sql_query = db.build_sql_query(
            select_clause=select_clause,
            from_clause=from_clause,
            where_conditions=where_conditions,
            order_by_column="total_amount",
            allowed_sort_columns=["total_amount", "order_count", "total_quantity"]
        )
        
        # Execute with parameters
        parameters = ('2024-01-01', '2024-03-31', 'USA', 50.00)
        results = db.execute_query(sql_query, parameters)
        
        if results is not None:
            # Save with custom settings
            db.save_results_to_csv(
                'sales_analysis.csv',
                include_index=True,
                delimiter=';'
            )


# Example 4: Error Handling
def example_with_error_handling():
    """
    Example showing how to handle potential errors when using the DatabaseManager.
    """
    connection_string = "Driver={SQL Server};Server=myserver;Database=mydatabase;UID=myuser;PWD=mypassword"
    
    db = DatabaseManager(connection_string)
    try:
        # Attempt to connect
        if not db.connect():
            print("Failed to connect to database")
            return
        
        try:
            # Build and execute query
            query = db.build_sql_query(
                select_clause="SELECT * FROM non_existent_table",
                from_clause=""
            )
            
            results = db.execute_query(query)
            
            if results is not None:
                if len(results) > 0:
                    print(f"Found {len(results)} rows")
                    db.save_results_to_csv('query_results.csv')
                else:
                    print("Query returned no results")
            else:
                print("Query execution failed")
                
        except Exception as e:
            print(f"Error during query execution: {e}")
            
    finally:
        db.close()


if __name__ == "__main__":
    # Run examples
    print("Running basic query example...")
    example_basic_query()
    
    print("\nRunning multiple queries example...")
    example_multiple_queries()
    
    print("\nRunning complex query example...")
    example_complex_query()
    
    print("\nRunning error handling example...")
    example_with_error_handling()

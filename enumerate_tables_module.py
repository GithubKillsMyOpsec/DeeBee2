import ibm_db

def enumerate_tables(conn_str):
    try:
        # Connect to the database
        conn = ibm_db.connect(conn_str, "", "")
        if conn:
            print("Connected to the database.")
            
            # Execute the SQL query to enumerate schemas
            schema_query = "SELECT SCHEMANAME FROM SYSCAT.SCHEMATA"
            schema_stmt = ibm_db.exec_immediate(conn, schema_query)
            
            # Fetch and iterate over schema names
            schema_row = ibm_db.fetch_tuple(schema_stmt)
            while schema_row:
                schema_name = schema_row[0]
                print("Tables in schema:", schema_name)
                
                # Execute the SQL query to enumerate tables in the current schema
                tables_query = f"SELECT TABNAME FROM SYSCAT.TABLES WHERE TABSCHEMA = '{schema_name}'"
                tables_stmt = ibm_db.exec_immediate(conn, tables_query)
                
                # Fetch and print table names
                table_row = ibm_db.fetch_tuple(tables_stmt)
                while table_row:
                    print("  ", table_row[0])
                    table_row = ibm_db.fetch_tuple(tables_stmt)
                
                schema_row = ibm_db.fetch_tuple(schema_stmt)  # Move to the next schema
            
            # Close the connection
            ibm_db.close(conn)
            print("Database connection closed.")
        else:
            print("Failed to connect to the database.")
    except Exception as e:
        print("An error occurred:", e)

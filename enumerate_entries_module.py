import ibm_db

def enumerate_entries(conn_str, schema_name, table_name):
    try:
        # Connect to the database
        conn = ibm_db.connect(conn_str, "", "")
        if conn:
            print("Connected to the database.")
            
            # Execute SQL query to select entries from the specified table in the specified schema
            query = f"SELECT * FROM {schema_name}.{table_name}"
            stmt = ibm_db.exec_immediate(conn, query)
            
            # Fetch and return the entries
            rows = []
            row = ibm_db.fetch_tuple(stmt)
            while row:
                rows.append(row)
                row = ibm_db.fetch_tuple(stmt)
            
            # Close the connection
            ibm_db.close(conn)
            print("Database connection closed.")
            return rows
        else:
            print("Failed to connect to the database.")
            return None
    except Exception as e:
        print("An error occurred:", e)
        return None

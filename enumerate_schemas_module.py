import ibm_db

def enumerate_schemas(conn_str):
    try:
        # Connect to the database
        conn = ibm_db.connect(conn_str, "", "")
        if conn:
            print("Connected to the database.")
            
            # Execute the SQL query to enumerate schemas
            sql_query = "SELECT SCHEMANAME FROM SYSCAT.SCHEMATA"
            stmt = ibm_db.exec_immediate(conn, sql_query)
            
            # Fetch and return the schema names
            schemas = []
            row = ibm_db.fetch_tuple(stmt)
            if row:
                print("Schemas in the database:")
                while row:
                    schemas.append(row[0])
                    print(row[0])
                    row = ibm_db.fetch_tuple(stmt)
                return schemas
            else:
                print("No schemas found in the database.")
                return None
            
            # Close the connection
            ibm_db.close(conn)
        else:
            print("Failed to connect to the database.")
            return None
    except Exception as e:
        print("An error occurred:", e)
        return None

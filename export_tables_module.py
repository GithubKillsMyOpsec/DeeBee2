import ibm_db
import csv

def export_tables(conn_str, output_dir):
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
                print("Exporting tables in schema:", schema_name)
                
                # Execute the SQL query to enumerate tables in the current schema
                tables_query = f"SELECT TABNAME FROM SYSCAT.TABLES WHERE TABSCHEMA = '{schema_name}'"
                tables_stmt = ibm_db.exec_immediate(conn, tables_query)
                
                # Fetch table names
                table_row = ibm_db.fetch_tuple(tables_stmt)
                while table_row:
                    table_name = table_row[0]
                    print("  Exporting table:", table_name)
                    
                    try:
                        # Execute the SQL query to export data from the current table
                        data_query = f"SELECT * FROM {schema_name}.{table_name}"
                        data_stmt = ibm_db.exec_immediate(conn, data_query)
                        
                        # Write data to CSV file
                        with open(f"{output_dir}/{table_name}.csv", 'w', newline='') as f:
                            writer = csv.writer(f)
                            writer.writerow([ibm_db.field_name(data_stmt, i) for i in range(ibm_db.num_fields(data_stmt))])
                            while ibm_db.fetch_row(data_stmt):
                                writer.writerow(ibm_db.fetch_tuple(data_stmt))
                    except Exception as e:
                        # Handle all exceptions
                        print(f"    An error occurred while exporting table {schema_name}.{table_name}: {e}")
                    
                    table_row = ibm_db.fetch_tuple(tables_stmt)  # Move to the next table
                
                schema_row = ibm_db.fetch_tuple(schema_stmt)  # Move to the next schema
            
            # Close the connection
            ibm_db.close(conn)
            print("Database export completed.")
        else:
            print("Failed to connect to the database.")
    except Exception as e:
        print("An error occurred:", e)

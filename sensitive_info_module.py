import ibm_db

def get_sensitive_info(conn_str):
    queries = {
        "ENV_SYS_INFO": "SELECT * FROM SYSIBMADM.ENV_SYS_INFO",
        "DBMCFG": "SELECT * FROM SYSIBMADM.DBMCFG",
        "DBCFG": "SELECT * FROM SYSIBMADM.DBCFG",
        "SNAPDB": "SELECT * FROM SYSIBMADM.SNAPDB",
        "SNAPAPPL": "SELECT * FROM SYSIBMADM.SNAPAPPL",
        "SNAPBP": "SELECT * FROM SYSIBMADM.SNAPBP",
        "SNAPLOCKWAIT": "SELECT * FROM SYSIBMADM.SNAPLOCKWAIT",
        "MON_CURRENT_SQL": "SELECT * FROM SYSIBMADM.MON_CURRENT_SQL",
        "MON_LOCKWAITS": "SELECT * FROM SYSIBMADM.MON_LOCKWAITS",
        "AUTHIDINFO": "SELECT * FROM SYSIBMADM.AUTHIDINFO",
        "AUTHORIZATIONS": "SELECT * FROM SYSIBMADM.AUTHORIZATIONS",
        "DBAUTH": "SELECT * FROM SYSCAT.DBAUTH",
        "TABAUTH": "SELECT * FROM SYSCAT.TABAUTH",
        "PACKAGEAUTH": "SELECT * FROM SYSCAT.PACKAGEAUTH",
        "INDEXAUTH": "SELECT * FROM SYSCAT.INDEXAUTH",
        "COLAUTH": "SELECT * FROM SYSCAT.COLAUTH",
        "SCHEMAAUTH": "SELECT * FROM SYSCAT.SCHEMAAUTH"
    }
    
    results = {}
    try:
        # Connect to the database
        conn = ibm_db.connect(conn_str, "", "")
        if conn:
            print("Connected to the database.")
            
            for key, query in queries.items():
                stmt = ibm_db.exec_immediate(conn, query)
                rows = []
                row = ibm_db.fetch_tuple(stmt)
                while row:
                    rows.append(row)
                    row = ibm_db.fetch_tuple(stmt)
                results[key] = rows
            
            # Close the connection
            ibm_db.close(conn)
            print("Database connection closed.")
            return results
        else:
            print("Failed to connect to the database.")
            return None
    except Exception as e:
        print("An error occurred:", e)
        return None

import ibm_db
import argparse
from enumerate_entries_module import enumerate_entries
from enumerate_schemas_module import enumerate_schemas
from enumerate_tables_module import enumerate_tables
from export_tables_module import export_tables
from system_info_module import get_system_info
from sensitive_info_module import get_sensitive_info



version = "0.5.2"
#TODO: Make a module to enumerate tables in user specified schema
#TODO: Make non-interactive mode work.


# Function to read connection parameters from a text file
def read_connection_params_from_file(file_path):
    params = {}
    with open(file_path, 'r') as file:
        for line in file:
            key, value = line.strip().split('=')
            params[key.strip()] = value.strip()
    return params

# Function to assemble the connection string
def assemble_connection_string(params):
    # Add the 'DATABASE' parameter to the connection string
    conn_str = f"DATABASE={params['database']};"
    # Add other parameters to the connection string
    conn_str += ";".join([f"{key.upper()}={value}" for key, value in params.items() if key != 'database'])
    return conn_str

def check_connection(conn_str):
    print("Starting Initial Connection Test...")
    try:
        conn = ibm_db.connect(conn_str, "", "")
        if conn:
            ibm_db.close(conn)
            print("Connection Successful!")
            return True
    except Exception as e:
        print("Connection error:", e)
    return False


def run_interactive_mode(conn_str):
    print("Interactive mode activated.")
    if not check_connection(conn_str):
        print("Failed to establish a connection. Exiting...")
        return
    
    while True:
        print("\n=======================================")
        print("\nSelect a module to run:")
        print("1. Enumerate database schemas")
        print("2. Enumerate tables in all schemas")
        print("3. Enumerate entries in a specific table")
        print("4. Export the database")
        print("5. Get system information")
        print("0. Exit")
        choice = input("Enter your choice: ")

        if choice == "3":
            schema_name = input("Enter the schema name: ")
            table_name = input("Enter the table name: ")
            rows = enumerate_entries(conn_str, schema_name, table_name)
            for row in rows:
                print(row)
        elif choice == "4":
            output_dir = input("Enter the directory to store CSV files: ")
            export_tables(conn_str, output_dir)
            print("Database export completed.")
        elif choice == "1":
            schemas = enumerate_schemas(conn_str)
            if schemas:
                print("Database schemas:")
                for schema in schemas:
                    print(schema)
        elif choice == "2":
            tables = enumerate_tables(conn_str)
            if tables:
                print("Tables in all schemas:")
                for schema, table in tables.items():
                    print(f"Schema: {schema}, Tables: {table}")
        elif choice == "5":
            system_info = get_system_info(conn_str)
            if system_info:
                print("System Information:")
                for info in system_info:
                    print(info)
        elif choice == "0":
            print("Thank you for using DeeBee2. Bye Bye!")
            break
        else:
            print("Invalid choice. Please try again.")

def run_non_interactive_mode(conn_str, module, **kwargs):
    print(f"Running {module} module in non-interactive mode.")
    if module == "enumerate_entries":
        enumerate_entries(conn_str, kwargs['schema_name'], kwargs['table_name'])
    elif module == "export_database":
        export_tables(conn_str)
    elif module == "get_system_info":
        system_info = get_system_info(conn_str)
        if system_info:
            print("System Information:")
            for info in system_info:
                print(info)
    elif module == "get_sensitive_info":
        sensitive_info = get_sensitive_info(conn_str)
        if sensitive_info:
            print("Sensitive Information:")
            for key, info in sensitive_info.items():
                print(f"{key}:")
                for row in info:
                    print(row)

def main():
    parser = argparse.ArgumentParser(description="Python CLI Application")
    parser.add_argument("--hostname", help="Database hostname")
    parser.add_argument("-p", "--port", help="Database port")
    parser.add_argument("--uid", help="User ID")
    parser.add_argument("--passw", help="Password")
    parser.add_argument("--database", help="Database name")
    parser.add_argument("--security", default="SSL", help="Security mode")
    parser.add_argument("--conn-file", help="Text file containing connection parameters")
    parser.add_argument("--interactive", action="store_true", help="Enable interactive mode")
    parser.add_argument("--module", help="Specify the module to run in non-interactive mode")
    print("     ____   __ __       _             ")
    print("    / __ \ / //_/___   (_)____   _____")
    print("   / /_/ // ,<  / _ \ / // __ \ / ___/")
    print("  / _, _// /| |/  __// // / / /(__  ) ")
    print(" /_/ |_|/_/ |_|\___//_//_/ /_//____/  ")

    print("IBM DB2 + SSL Enumeration/Recovery Tool")
    print("Version " + version)
    args = parser.parse_args()

    if not args.hostname and not args.conn_file:
        parser.error("Please specify the database hostname using --hostname or provide a connection file using --conn-file.")
    
    if args.conn_file:
        conn_params = read_connection_params_from_file(args.conn_file)
    else:
        conn_params = {
            "hostname": args.hostname,
            "port": args.port,
            "uid": args.uid,
            "pwd": args.passw,
            "database": args.database,
            "security": args.security
        }
    
    conn_str = assemble_connection_string(conn_params)

    if args.interactive:
        run_interactive_mode(conn_str)
    elif args.module:
        if args.module not in ["enumerate_entries", "export_database", "get_system_info", "get_sensitive_info"]:
            parser.error("Invalid module specified.")
        run_non_interactive_mode(conn_str, args.module)
    else:
        parser.error("Please specify either --interactive or --module.")

if __name__ == "__main__":
    main()


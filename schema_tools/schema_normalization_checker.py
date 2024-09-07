import psycopg2
from psycopg2 import sql

# Database connection details
DB_HOST = "localhost"
DB_NAME = "trading_bot_db"
DB_USER = "postgres"
DB_PASSWORD = "dildobaggins"

def get_connection():
    """Establish a connection to the PostgreSQL database."""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        raise

def get_tables_with_composite_keys(conn):
    """Retrieve tables with composite primary keys."""
    query = """
    SELECT 
        kcu.table_schema,
        kcu.table_name,
        kcu.column_name,
        tc.constraint_name
    FROM 
        information_schema.table_constraints tc
    JOIN information_schema.key_column_usage kcu 
        ON tc.constraint_name = kcu.constraint_name
        AND tc.table_schema = kcu.table_schema
    WHERE 
        tc.constraint_type = 'PRIMARY KEY'
    GROUP BY 
        kcu.table_schema, kcu.table_name, tc.constraint_name, kcu.column_name
    HAVING 
        COUNT(kcu.column_name) > 1;
    """

    with conn.cursor() as cur:
        cur.execute(query)
        tables = cur.fetchall()

    return tables

def check_partial_dependencies(conn, table_name, columns):
    """Check for partial dependencies in a table."""
    primary_key_columns = set(columns)
    with conn.cursor() as cur:
        cur.execute(sql.SQL("SELECT column_name FROM information_schema.columns WHERE table_name = %s;"), [table_name])
        all_columns = set([row[0] for row in cur.fetchall()])
    
    non_primary_key_columns = all_columns - primary_key_columns

    for col in non_primary_key_columns:
        for pk_col in primary_key_columns:
            cur.execute(sql.SQL(f"SELECT DISTINCT {col} FROM {table_name} GROUP BY {pk_col}"))
            if cur.rowcount > 1:
                print(f"Partial dependency found in table {table_name}: {col} depends on {pk_col}")
                break

def check_transitive_dependencies(conn, table_name):
    """Check for transitive dependencies in a table."""
    with conn.cursor() as cur:
        # Get the primary key columns
        cur.execute(sql.SQL("SELECT kcu.column_name FROM information_schema.key_column_usage kcu WHERE kcu.table_name = %s AND kcu.constraint_name IN (SELECT tc.constraint_name FROM information_schema.table_constraints tc WHERE tc.table_name = %s AND tc.constraint_type = 'PRIMARY KEY');"), [table_name, table_name])
        primary_key_columns = [row[0] for row in cur.fetchall()]

        # Get all non-primary key columns
        cur.execute(sql.SQL("SELECT column_name FROM information_schema.columns WHERE table_name = %s;"), [table_name])
        all_columns = [row[0] for row in cur.fetchall()]
        non_primary_key_columns = [col for col in all_columns if col not in primary_key_columns]

        # Check for transitive dependencies
        for col1 in non_primary_key_columns:
            for col2 in non_primary_key_columns:
                if col1 != col2:
                    cur.execute(sql.SQL(f"SELECT DISTINCT {col1} FROM {table_name} GROUP BY {col2}"))
                    if cur.rowcount > 1:
                        print(f"Transitive dependency found in table {table_name}: {col1} depends on {col2}, which may be a violation of 3NF.")
                        break

def main():
    conn = get_connection()
    tables = get_tables_with_composite_keys(conn)
    print(f"Tables with composite primary keys: {tables}")
    
    for table in tables:
        table_name = table[1]
        columns = [t[2] for t in tables if t[1] == table_name]
        check_partial_dependencies(conn, table_name, columns)
        check_transitive_dependencies(conn, table_name)
    
    conn.close()

if __name__ == "__main__":
    main()

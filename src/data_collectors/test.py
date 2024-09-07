import psycopg2

try:
    conn = psycopg2.connect(
        host="localhost",
        dbname="trading_bot_db",
        user="postgres",
        password="dildobaggins"  # Replace with your actual password
    )
    print("Connection successful!")
    conn.close()
except Exception as e:
    print(f"Connection failed: {e}")

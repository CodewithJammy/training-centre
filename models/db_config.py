import os
import pyodbc

def get_connection():
    # Read connection string from Azure App Service settings
    database_url = os.getenv("db_url")

    if not database_url:
        raise RuntimeError("DATABASE_URL is not set in App Service configuration")

    # Connect directly with pyodbc
    conn = pyodbc.connect(database_url)
    return conn

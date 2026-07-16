import urllib
from sqlalchemy import create_engine

connection_string = (
    "Driver={ODBC Driver 18 for SQL Server};"
    "Server=tcp:questionbank777.database.windows.net,1433;"
    "Database=questionBank;"
    "Uid=CloudSA2ff8cbc8;"
    "Pwd=Cyber@#12345;"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "Connection Timeout=30;"
)

params = urllib.parse.quote_plus(connection_string)
engine = create_engine("mssql+pyodbc:///?odbc_connect=" + params)

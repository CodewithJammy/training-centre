# models/db_config.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    user = "CloudSA2ff8cbc8@questionbank777"
    password = "Cyber@#12345"
    server = "questionbank777.database.windows.net"
    database = "questionBank"

    # URL encode user and password
    user_enc = urllib.parse.quote_plus(user)
    password_enc = urllib.parse.quote_plus(password)

    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"mssql+pyodbc://{user_enc}:{password_enc}@{server}:1433/{database}"
        "?driver=ODBC+Driver+18+for+SQL+Server&Encrypt=yes&TrustServerCertificate=no&Connection+Timeout=30"
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # app.config['SQLALCHEMY_DATABASE_URI'] = (
    #    "mssql+pyodbc://CloudSA2ff8cbc8%40questionbank777:Cyber%40%2312345@questionbank777.database.windows.net:1433/questionBank"
    #   "?driver=ODBC+Driver+18+for+SQL+Server&Encrypt=yes&TrustServerCertificate=no&Connection+Timeout=30"
    #)
    #  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

# models/db_config.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        "mssql+pyodbc://CloudSA2ff8cbc8%40questionbank777:Cyber%40%2312345@questionbank777.database.windows.net:1433/questionBank"
        "?driver=ODBC+Driver+18+for+SQL+Server&Encrypt=yes&TrustServerCertificate=no"
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

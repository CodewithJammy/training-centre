from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    # Azure SQL connection string with Entra Integrated Authentication
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        "mssql+pyodbc://@questionbank777.database.windows.net/questionBank"
        "?driver=ODBC+Driver+18+for+SQL+Server&authentication=ActiveDirectoryIntegrated"
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return db

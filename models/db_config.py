from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    # Azure SQL connection string
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        "mssql+pyodbc://examadmin:YourStrongPassword123@examportal-sqlserver.database.windows.net/ExamDB"
        "?driver=ODBC+Driver+18+for+SQL+Server"
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return db

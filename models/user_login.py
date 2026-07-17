from models.db_config import db

class UserLogin(db.Model):
    __tablename__ = "UserLogin"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    mobile = db.Column(db.String(15), unique=True, nullable=False)

from db_config import db

class ExamQuestion(db.Model):
    __tablename__ = 'ExamQuestions'
    QuestionID = db.Column(db.Integer, primary_key=True)
    Section = db.Column(db.String(50), nullable=False)
    QuestionText = db.Column(db.Text)
    QuestionImage = db.Column(db.String(500))
    OptionAText = db.Column(db.String(255))
    OptionAImage = db.Column(db.String(500))
    OptionBText = db.Column(db.String(255))
    OptionBImage = db.Column(db.String(500))
    OptionCText = db.Column(db.String(255))
    OptionCImage = db.Column(db.String(500))
    OptionDText = db.Column(db.String(255))
    OptionDImage = db.Column(db.String(500))
    CorrectOption = db.Column(db.String(1), nullable=False)

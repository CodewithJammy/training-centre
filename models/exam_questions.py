from models.db_config import get_connection

def get_all_questions():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT QuestionID, Section, QuestionText, CorrectOption FROM ExamQuestions")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_question_by_id(question_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ExamQuestions WHERE QuestionID=?", (question_id,))
    row = cursor.fetchone()
    conn.close()
    return row

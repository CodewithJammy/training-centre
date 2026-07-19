import pyodbc
from flask import Flask, request
from models.db_config import get_connection
app = Flask(__name__)

conn_str = "Driver={ODBC Driver 17 for SQL Server};Server=YOUR_SERVER;Database=YOUR_DB;UID=USER;PWD=PASS;"
def get_connection():
    return pyodbc.connect(conn_str)

@app.route('/register', methods=['POST'])
def register():
    fullname = request.form['name']
    username = request.form['email']
    mobile = request.form['mobile']
    course = request.form['course']
    message = request.form.get('message', '')

    # For now, mark payment as Pending
    amount = 0  # you can map course → fee later
    expiredate = None  # will set after payment success

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Subscriber (fullname, username, mobile, course, message, payment_status, amount, date, expiredate)
        VALUES (?, ?, ?, ?, ?, ?, ?, GETDATE(), ?)
    """, fullname, username, mobile, course, message, 'Pending', amount, expiredate)
    conn.commit()
    conn.close()

    return f"Hello {fullname}, you are registered successfully! Payment pending."

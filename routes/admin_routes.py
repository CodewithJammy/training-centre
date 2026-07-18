import re
import logging
from flask import Blueprint, render_template, request, redirect, url_for, session
from models.exam_questions import ExamQuestion
from models.user_login import UserLogin
from models.db_config import get_connection
from werkzeug.security import check_password_hash
from sqlalchemy.exc import IntegrityError

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

# --- LOGIN ---
@admin_bp.route("/login", methods=["GET", "POST"])


def login():
    username = request.form["username"]
    password = request.form["password"]

    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Run query safely with parameters
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        row = cursor.fetchone()
        conn.close()

        if row:
            # Successful login → redirect to dashboard
            return redirect(url_for("admin.add_question"))
        else:
            # Failed login → show error on index.html
            return render_template("index.html", error="Invalid credentials")
    except Exception as e:
        return render_template("index.html", error=f"Database error: {e}")


# --- ADD QUESTION ---
@admin_bp.route("/add-question", methods=["GET", "POST"])
def add_question():
    print("Request method:", request.method, "Path:", request.path)
    if "admin_user" not in session:
        return redirect(url_for("admin.login"))

    if request.method == "POST":
        section = request.form["section"]
        question_text = request.form.get("question_text")

        existing = ExamQuestion.query.filter_by(Section=section, QuestionText=question_text).first()
        if existing:
            return render_template("admin_form.html", error=f"Duplicate question in section {section}")

        q = ExamQuestion(
            Section=section,
            QuestionText=question_text,
            QuestionImage=request.form.get("question_image"),
            OptionAText=request.form.get("option_a_text"),
            OptionAImage=request.form.get("option_a_image"),
            OptionBText=request.form.get("option_b_text"),
            OptionBImage=request.form.get("option_b_image"),
            OptionCText=request.form.get("option_c_text"),
            OptionCImage=request.form.get("option_c_image"),
            OptionDText=request.form.get("option_d_text"),
            OptionDImage=request.form.get("option_d_image"),
            CorrectOption=request.form["correct_option"]
        )
        try:
            db.session.add(q)
            db.session.commit()
            return redirect("/admin/list")
        except IntegrityError:
            db.session.rollback()
            return render_template("admin_form.html", error="Duplicate entry detected")

    return render_template("admin_form.html")

# --- LIST QUESTIONS ---

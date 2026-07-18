import re
import logging
from flask import Blueprint, render_template, request, redirect, url_for, session
from models.db_config import get_connection
from werkzeug.security import check_password_hash
from models.exam_questions import get_all_questions, get_question_by_id


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
from flask import request, redirect, url_for, render_template, session
from models.db_config import get_connection

def add_question():
    print("Request method:", request.method, "Path:", request.path)
    if "admin_user" not in session:
        return redirect(url_for("admin.login"))

    if request.method == "POST":
        section = request.form["section"]
        question_text = request.form.get("question_text")

        try:
            conn = get_connection()
            cursor = conn.cursor()

            # Check for duplicate
            cursor.execute(
                "SELECT 1 FROM ExamQuestions WHERE Section=? AND QuestionText=?",
                (section, question_text)
            )
            existing = cursor.fetchone()
            if existing:
                conn.close()
                return render_template("admin_form.html", error=f"Duplicate question in section {section}")

            # Insert new question
            cursor.execute("""
                INSERT INTO ExamQuestions
                (Section, QuestionText, QuestionImage,
                 OptionAText, OptionAImage,
                 OptionBText, OptionBImage,
                 OptionCText, OptionCImage,
                 OptionDText, OptionDImage,
                 CorrectOption)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                section,
                question_text,
                request.form.get("question_image"),
                request.form.get("option_a_text"),
                request.form.get("option_a_image"),
                request.form.get("option_b_text"),
                request.form.get("option_b_image"),
                request.form.get("option_c_text"),
                request.form.get("option_c_image"),
                request.form.get("option_d_text"),
                request.form.get("option_d_image"),
                request.form["correct_option"]
            ))

            conn.commit()
            conn.close()
            return redirect("/admin/list")

        except Exception as e:
            # Rollback if error
            conn.rollback()
            conn.close()
            return render_template("admin_form.html", error=f"Database error: {e}")

    return render_template("admin_form.html")

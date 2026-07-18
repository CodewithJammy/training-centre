import logging
from flask import Blueprint, render_template, request, session, redirect, url_for
from models.db_config import get_connection

# Create blueprint
exam_bp = Blueprint("exam", __name__, url_prefix="/exam")

# --- Exam Home Page ---
@exam_bp.route("/", methods=["GET"])
def exam_home():
    if "admin_user" not in session:
        # If you want only logged-in users to access exam
        return redirect(url_for("admin.login"))

    return render_template("exam.html")  # your HTML page

# --- Load Questions by Section ---
@exam_bp.route("/section/<string:section>", methods=["GET"])
def load_section(section):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Fetch questions for the given section
        cursor.execute("""
            SELECT QuestionID, Section, QuestionText, QuestionImage,
                   OptionAText, OptionAImage,
                   OptionBText, OptionBImage,
                   OptionCText, OptionCImage,
                   OptionDText, OptionDImage,
                   CorrectOption
            FROM ExamQuestions
            WHERE Section = ?
        """, (section,))
        rows = cursor.fetchall()
        conn.close()

        # Pass questions to template
        return render_template("exam_section.html", section=section, questions=rows)

    except Exception as e:
        logging.error(f"Error loading section {section}: {e}")
        return render_template("exam_section.html", section=section, error=f"Database error: {e}")

# --- Submit Answer ---
@exam_bp.route("/submit/<int:qid>", methods=["POST"])
def submit_answer(qid):
    selected_option = request.form.get("selected_option")
    # You can store answers in session or DB
    answers = session.get("answers", {})
    answers[qid] = selected_option
    session["answers"] = answers

    return redirect(url_for("exam.exam_home"))

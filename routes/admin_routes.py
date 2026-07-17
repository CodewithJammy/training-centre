import re
from flask import Blueprint, render_template, request, redirect, url_for, session
from models.exam_questions import ExamQuestion
from models.user_login import UserLogin
from models.db_config import db
from werkzeug.security import check_password_hash
from sqlalchemy.exc import IntegrityError

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

# --- LOGIN ---
@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = UserLogin.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            # ✅ Email format check
            email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
            if not re.match(email_pattern, user.email):
                return render_template("index.html", error="Invalid email format")

            # ✅ Mobile check (India default: +91 and 10 digits)
            mobile_pattern = r"^\+91\d{10}$"
            if not re.match(mobile_pattern, user.mobile):
                return render_template("index.html", error="Invalid mobile number (must be +91XXXXXXXXXX)")

            session["admin_user"] = username
            return redirect(url_for("admin.exam_questions"))
        else:
            return render_template("index.html", error="Invalid credentials")

    return render_template("login.html")

# --- ADD QUESTION ---
@admin_bp.route("/add-question", methods=["GET", "POST"])
def add_question():
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
@admin_bp.route("/list")
def list_questions():
    if "admin_user" not in session:
        return redirect(url_for("admin.login"))
    questions = ExamQuestion.query.all()
    return render_template("admin_list.html", questions=questions)
#-------------------------------------------------

    questions = ExamQuestion.query.all()
    return render_template("admin_list.html", questions=questions)

from flask import Blueprint, render_template, request, redirect
from models.exam_question import ExamQuestion, db

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

@admin_bp.route("/add-question", methods=["GET", "POST"])
def add_question():
    if request.method == "POST":
        q = ExamQuestion(
            Section=request.form["section"],
            QuestionText=request.form.get("question_text"),
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
        db.session.add(q)
        db.session.commit()
        return redirect("/admin/list")
    return render_template("admin_form.html")

@admin_bp.route("/list")
def list_questions():
    questions = ExamQuestion.query.all()
    return render_template("admin_list.html", questions=questions)

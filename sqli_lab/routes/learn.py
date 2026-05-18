from flask import Blueprint, render_template, request, redirect, url_for, flash

from sqli_lab.auth_utils import login_required, current_user
from sqli_lab.lessons import LESSONS, get_lesson

learn_bp = Blueprint("learn", __name__)


@learn_bp.route("/learn")
@login_required
def learn_index():
    return render_template("learn/index.html", lessons=LESSONS, user=current_user())


@learn_bp.route("/learn/<slug>", methods=["GET", "POST"])
@login_required
def learn_detail(slug):
    lesson = get_lesson(slug)
    if not lesson:
        flash("Lesson not found.", "error")
        return redirect(url_for("learn.learn_index"))

    quiz_result = None
    if request.method == "POST":
        try:
            chosen = int(request.form.get("answer", "-1"))
        except ValueError:
            chosen = -1
        correct = chosen == lesson["quiz"]["answer"]
        quiz_result = "correct" if correct else "incorrect"
        if correct:
            flash("Quiz passed!", "success")
        else:
            flash("Try again — review the lesson.", "warning")

    return render_template(
        "learn/detail.html",
        lesson=lesson,
        user=current_user(),
        quiz_result=quiz_result,
    )

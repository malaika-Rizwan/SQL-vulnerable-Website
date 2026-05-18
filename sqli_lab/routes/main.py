from flask import Blueprint, render_template, session, redirect, url_for

from sqli_lab.auth_utils import current_user, login_required
from sqli_lab.models import Challenge, Progress

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    return render_template("index.html", user=current_user())


@main_bp.route("/dashboard")
@login_required
def dashboard():
    user = current_user()
    completed = Progress.query.filter_by(user_id=user.id).count()
    total = Challenge.query.count()
    return render_template(
        "dashboard.html",
        user=user,
        completed=completed,
        total=total,
    )

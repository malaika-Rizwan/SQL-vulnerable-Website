from flask import Blueprint, render_template, request, redirect, url_for, flash, session

from sqli_lab.auth_utils import (
    check_password,
    hash_password,
    login_required,
    login_user,
    logout_user,
    current_user,
)
from sqli_lab.models import User, db
from sqli_lab.rate_limit import check_rate_limit

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_id"):
        return redirect(url_for("main.dashboard"))

    if request.method == "POST":
        ip = request.remote_addr or "unknown"
        if not check_rate_limit(f"login:{ip}", max_attempts=8, window_seconds=60):
            flash("Too many login attempts. Wait a minute.", "error")
            return render_template("login.html"), 429

        username = (request.form.get("username") or "").strip()
        password = request.form.get("password") or ""
        user = User.query.filter_by(username=username).first()
        if user and check_password(password, user.password_hash):
            login_user(user)
            flash("Welcome back.", "success")
            nxt = request.args.get("next") or url_for("main.dashboard")
            return redirect(nxt)
        flash("Invalid username or password.", "error")

    return render_template("login.html")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if session.get("user_id"):
        return redirect(url_for("main.dashboard"))

    if request.method == "POST":
        username = (request.form.get("username") or "").strip()
        password = request.form.get("password") or ""
        if len(username) < 3 or len(password) < 6:
            flash("Username (3+) and password (6+) required.", "error")
            return render_template("register.html")
        if User.query.filter_by(username=username).first():
            flash("Username already taken.", "error")
            return render_template("register.html")
        user = User(username=username, password_hash=hash_password(password))
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash("Account created. Start learning!", "success")
        return redirect(url_for("main.dashboard"))

    return render_template("register.html")


@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    flash("Logged out.", "success")
    return redirect(url_for("main.index"))

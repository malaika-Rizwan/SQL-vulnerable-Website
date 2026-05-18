import bcrypt
from flask import session, redirect, url_for, flash, request
from functools import wraps

from sqli_lab.models import User, db


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def check_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password.encode(), password_hash.encode())


def login_user(user: User) -> None:
    session.permanent = True
    session["user_id"] = user.id
    session["username"] = user.username


def logout_user() -> None:
    session.clear()


def current_user() -> User | None:
    uid = session.get("user_id")
    if not uid:
        return None
    return db.session.get(User, uid)


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("user_id"):
            flash("Please log in to access the lab.", "warning")
            return redirect(url_for("auth.login", next=request.path))
        return view(*args, **kwargs)

    return wrapped

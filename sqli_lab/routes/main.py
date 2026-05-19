from flask import Blueprint, render_template, session, redirect, url_for

from sqli_lab.auth_utils import current_user, login_required
from sqli_lab.track_service import build_track_view, track_progress

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    user = current_user()
    track = build_track_view(user)
    done, total = track_progress(user)
    return render_template(
        "index.html",
        user=user,
        track=track,
        track_done=done,
        track_total=total,
        guest_mode=user is None,
    )


@main_bp.route("/dashboard")
@login_required
def dashboard():
    user = current_user()
    track = build_track_view(user)
    done, total = track_progress(user)
    return render_template(
        "dashboard.html",
        user=user,
        track=track,
        track_done=done,
        track_total=total,
    )

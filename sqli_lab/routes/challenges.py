from flask import Blueprint, render_template, request, flash, current_app, session

from sqli_lab.auth_utils import login_required, current_user
from sqli_lab.models import Challenge, Progress
from sqli_lab.services import submit_flag
from sqli_lab.vuln import queries as vuln

challenges_bp = Blueprint("challenges", __name__)

HANDLERS = {
    "error-based": lambda db, req: vuln.error_based_lookup(db, req.form.get("input", "")),
    "union-based": lambda db, req: vuln.union_product_search(db, req.form.get("input", "")),
    "boolean-blind": lambda db, req: vuln.boolean_profile_exists(db, req.form.get("input", "")),
    "time-based": lambda db, req: vuln.time_based_check(db, req.form.get("input", "")),
    "auth-bypass": lambda db, req: vuln.auth_bypass_login(
        db, req.form.get("username", ""), req.form.get("password", "")
    ),
    "second-order": lambda db, req: _second_order(db, req),
    "stacked-queries": lambda db, req: vuln.stacked_multi_statement(
        db,
        req.form.get("input", ""),
        session.get("advanced_mode", False),
    ),
}


def _second_order(db_path, req):
    if req.form.get("step") == "store":
        return vuln.second_order_store_comment(
            db_path, req.form.get("username", ""), req.form.get("body", "")
        )
    return vuln.second_order_render(db_path, req.form.get("username", ""))


@challenges_bp.route("/challenges")
@login_required
def challenges_index():
    user = current_user()
    from sqli_lab.track import get_track_slugs

    all_ch = (
        Challenge.query.filter(Challenge.slug.in_(get_track_slugs()))
        .order_by(Challenge.order_index)
        .all()
    )
    done_ids = {
        p.challenge_id
        for p in Progress.query.filter_by(user_id=user.id).all()
    }
    return render_template(
        "challenges/index.html",
        challenges=all_ch,
        done_ids=done_ids,
        user=user,
    )


@challenges_bp.route("/challenges/<slug>", methods=["GET", "POST"])
@login_required
def challenge_detail(slug):
    challenge = Challenge.query.filter_by(slug=slug, practice=False).first_or_404()
    db_path = current_app.config["LAB_DB_PATH"]
    lab_result = None

    if request.method == "POST":
        action = request.form.get("action")
        if action == "advanced":
            session["advanced_mode"] = request.form.get("enable") == "1"
            flash("Advanced mode updated.", "success")
        elif action == "lab" and challenge.sqli_type in HANDLERS:
            if challenge.sqli_type == "out-of-band":
                flash("Out-of-band is concept-only in this lab.", "warning")
            else:
                lab_result = HANDLERS[challenge.sqli_type](db_path, request)
        elif action == "flag":
            result = submit_flag(current_user(), challenge, request.form.get("flag", ""))
            if result["correct"]:
                flash(f"Challenge complete! +{result['points_awarded']} pts", "success")
            else:
                flash("Wrong flag — keep trying (unlimited attempts).", "error")
            return render_template(
                "challenges/detail.html",
                challenge=challenge,
                user=current_user(),
                lab_result=lab_result,
                flag_result=result,
                advanced=session.get("advanced_mode", False),
            )

    completed = (
        Progress.query.filter_by(
            user_id=current_user().id, challenge_id=challenge.id
        ).first()
        is not None
    )
    return render_template(
        "challenges/detail.html",
        challenge=challenge,
        user=current_user(),
        lab_result=lab_result,
        flag_result=None,
        advanced=session.get("advanced_mode", False),
        completed=completed,
    )

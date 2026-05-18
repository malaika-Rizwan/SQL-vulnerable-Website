from flask import Blueprint, render_template, request, flash, current_app

from sqli_lab.auth_utils import login_required, current_user
from sqli_lab.models import Challenge
from sqli_lab.services import submit_flag
from sqli_lab.vuln import queries as vuln

practice_bp = Blueprint("practice", __name__)

PRACTICE_HANDLERS = {
    "error-based-intro": ("secret_id", lambda db, v: vuln.error_based_lookup(db, v)),
    "union-intro": ("keyword", lambda db, v: vuln.union_product_search(db, v)),
    "boolean-intro": ("username", lambda db, v: vuln.boolean_profile_exists(db, v)),
    "auth-bypass-intro": ("pair", None),
}


@practice_bp.route("/practice")
@login_required
def practice_index():
    items = Challenge.query.filter_by(practice=True).order_by(Challenge.order_index).all()
    return render_template("practice/index.html", challenges=items, user=current_user())


@practice_bp.route("/practice/<slug>", methods=["GET", "POST"])
@login_required
def practice_detail(slug):
    challenge = Challenge.query.filter_by(slug=slug, practice=True).first_or_404()
    db_path = current_app.config["LAB_DB_PATH"]
    lab_result = None
    flag_result = None

    if request.method == "POST":
        action = request.form.get("action")
        if action == "lab":
            if slug == "error-based-intro":
                lab_result = vuln.error_based_lookup(db_path, request.form.get("secret_id", ""))
            elif slug == "union-intro":
                lab_result = vuln.union_product_search(db_path, request.form.get("keyword", ""))
            elif slug == "boolean-intro":
                lab_result = vuln.boolean_profile_exists(db_path, request.form.get("username", ""))
            elif slug == "auth-bypass-intro":
                lab_result = vuln.auth_bypass_login(
                    db_path,
                    request.form.get("username", ""),
                    request.form.get("password", ""),
                )
            elif slug == "time-based-intro":
                lab_result = vuln.time_based_check(db_path, request.form.get("username", ""))
            elif slug == "second-order-intro":
                if request.form.get("step") == "store":
                    lab_result = vuln.second_order_store_comment(
                        db_path,
                        request.form.get("username", ""),
                        request.form.get("body", ""),
                    )
                else:
                    lab_result = vuln.second_order_render(db_path, request.form.get("username", ""))
        elif action == "flag":
            flag_result = submit_flag(current_user(), challenge, request.form.get("flag", ""))
            if flag_result["correct"]:
                flash(f"Correct! +{flag_result['points_awarded']} points", "success")
            else:
                flash("Incorrect flag.", "error")

    return render_template(
        "practice/detail.html",
        challenge=challenge,
        user=current_user(),
        lab_result=lab_result,
        flag_result=flag_result,
    )

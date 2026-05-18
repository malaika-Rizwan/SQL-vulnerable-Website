from flask import Blueprint, jsonify, request, current_app

from sqli_lab.auth_utils import login_required, current_user
from sqli_lab.models import Challenge, User
from sqli_lab.rate_limit import check_rate_limit
from sqli_lab.services import submit_flag
from sqli_lab.scoring import parse_badges
from sqli_lab.vuln import queries as vuln

api_bp = Blueprint("api", __name__)


def api_error(message: str, status: int = 400):
    return jsonify({"ok": False, "error": message}), status


@api_bp.route("/health")
def health():
    return jsonify({"ok": True, "service": "sqli-lab-python"})


@api_bp.route("/leaderboard")
@login_required
def api_leaderboard():
    rows = User.query.order_by(User.total_score.desc()).limit(20).all()
    return jsonify(
        {
            "ok": True,
            "data": [
                {
                    "username": u.username,
                    "total_score": u.total_score,
                    "badges": parse_badges(u.badges or ""),
                    "last_activity": u.last_activity.isoformat(),
                }
                for u in rows
            ],
        }
    )


@api_bp.route("/challenges/<slug>/submit", methods=["POST"])
@login_required
def api_submit(slug):
    ip = request.remote_addr or "unknown"
    if not check_rate_limit(f"submit:{ip}", max_attempts=20, window_seconds=60):
        return api_error("Rate limit exceeded", 429)

    challenge = Challenge.query.filter_by(slug=slug).first()
    if not challenge:
        return api_error("Challenge not found", 404)

    payload = request.get_json(silent=True) or {}
    flag = (payload.get("flag") or request.form.get("flag") or "").strip()
    if not flag:
        return api_error("flag required")

    result = submit_flag(current_user(), challenge, flag)
    return jsonify({"ok": True, **result})


@api_bp.route("/lab/<slug>/probe", methods=["POST"])
@login_required
def api_lab_probe(slug):
    db_path = current_app.config["LAB_DB_PATH"]
    payload = request.get_json(silent=True) or request.form
    mapping = {
        "error-based": lambda: vuln.error_based_lookup(db_path, payload.get("input", "")),
        "union-based": lambda: vuln.union_product_search(db_path, payload.get("input", "")),
    }
    if slug not in mapping:
        return api_error("Unknown lab endpoint", 404)
    return jsonify({"ok": True, "result": mapping[slug]()})

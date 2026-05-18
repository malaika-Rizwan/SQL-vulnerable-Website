from flask import Blueprint, render_template

from sqli_lab.auth_utils import login_required, current_user
from sqli_lab.models import User
from sqli_lab.scoring import parse_badges

leaderboard_bp = Blueprint("leaderboard", __name__)


@leaderboard_bp.route("/leaderboard")
@login_required
def leaderboard():
    # Safe ORM query — no string-concatenated SQL
    rows = (
        User.query.order_by(User.total_score.desc(), User.last_activity.desc())
        .limit(50)
        .all()
    )
    enriched = [
        {
            "username": u.username,
            "total_score": u.total_score,
            "streak": u.streak,
            "badges": parse_badges(u.badges or ""),
            "last_activity": u.last_activity,
            "is_you": u.id == current_user().id,
        }
        for u in rows
    ]
    return render_template(
        "leaderboard.html",
        rows=enriched,
        user=current_user(),
        scoring_rules={
            "base": "Challenge points on first correct flag only",
            "streak": "+5 per streak day, max +25 bonus",
            "retry": "Same flag resubmission does not add points",
        },
    )

from datetime import datetime, timezone

from sqli_lab.models import Challenge, Progress, Submission, User, db
from sqli_lab.scoring import add_badge, total_with_streak


def submit_flag(user: User, challenge: Challenge, flag: str) -> dict:
    flag = flag.strip()
    correct = flag == challenge.flag
    already = (
        Progress.query.filter_by(user_id=user.id, challenge_id=challenge.id).first()
        is not None
    )

    submission = Submission(
        user_id=user.id,
        challenge_id=challenge.id,
        submitted_flag=flag,
        correct=correct,
        points_awarded=0,
    )

    if correct:
        points = total_with_streak(challenge.points, user.streak, already)
        submission.points_awarded = points
        if not already:
            user.total_score += points
            user.streak = (user.streak or 0) + 1
            prog = Progress(user_id=user.id, challenge_id=challenge.id)
            db.session.add(prog)
            badge = f"{challenge.sqli_type}-solver"
            user.badges = add_badge(user.badges or "", badge)
    else:
        user.streak = 0

    user.last_activity = datetime.now(timezone.utc)
    db.session.add(submission)
    db.session.commit()

    return {
        "correct": correct,
        "points_awarded": submission.points_awarded,
        "already_completed": already and correct,
        "total_score": user.total_score,
    }

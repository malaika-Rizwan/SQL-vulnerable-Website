from sqli_lab.models import Challenge, Progress
from sqli_lab.track import TRACK_LABS, get_track_slugs


def build_track_view(user) -> list[dict]:
    """Build PortSwigger-style track rows with completion state."""
    slugs = get_track_slugs()
    challenges = {c.slug: c for c in Challenge.query.filter(Challenge.slug.in_(slugs)).all()}
    done_ids: set[int] = set()
    if user:
        done_ids = {p.challenge_id for p in Progress.query.filter_by(user_id=user.id).all()}

    statuses = []
    for meta in TRACK_LABS:
        ch = challenges.get(meta["slug"])
        completed = bool(ch and ch.id in done_ids)
        statuses.append((meta, ch, completed))

    first_open = len(TRACK_LABS)
    for i, (_, _, completed) in enumerate(statuses):
        if not completed:
            first_open = i
            break

    rows = []
    for i, (meta, ch, completed) in enumerate(statuses):
        if not user:
            locked = True
        else:
            locked = i > first_open

        rows.append(
            {
                **meta,
                "challenge": ch,
                "completed": completed,
                "locked": locked,
                "active": user is not None and i == first_open and not completed,
                "url": (
                    f"/challenges/{meta['slug']}"
                    if ch and user and not locked
                    else None
                ),
            }
        )

    return rows


def track_progress(user) -> tuple[int, int]:
    rows = build_track_view(user)
    done = sum(1 for r in rows if r["completed"])
    return done, len(TRACK_LABS)

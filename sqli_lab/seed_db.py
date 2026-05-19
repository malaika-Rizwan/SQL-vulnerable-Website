"""Database seed — PortSwigger-style 8-lab track + practice sandboxes."""

import json

from sqli_lab.auth_utils import hash_password
from sqli_lab.models import Challenge, User, db
from sqli_lab.track import TRACK_LABS

PRACTICE_LABS = [
    {
        "slug": "practice-error",
        "title": "Sandbox: Error-based warm-up",
        "sqli_type": "error-based",
        "difficulty": "easy",
        "points": 40,
        "flag": "FLAG{error_based_alpha}",
        "hints": json.dumps(["Try a single quote in the ID field."]),
        "description": "Warm-up before the track. Extract a flag from lab_secrets.",
        "practice": True,
        "order_index": 101,
    },
    {
        "slug": "practice-union",
        "title": "Sandbox: UNION warm-up",
        "sqli_type": "union-based",
        "difficulty": "easy",
        "points": 40,
        "flag": "FLAG{union_product_leak}",
        "hints": json.dumps(["Probe column count with ORDER BY or UNION NULL."]),
        "description": "Practice UNION before track labs 3–4.",
        "practice": True,
        "order_index": 102,
    },
]


def _track_challenge(meta: dict) -> dict:
    return {
        "slug": meta["slug"],
        "title": meta["title"],
        "sqli_type": meta["sqli_type"],
        "difficulty": meta["difficulty"],
        "points": meta["points"],
        "flag": meta["flag"],
        "hints": json.dumps(
            [
                f"PortSwigger topic: {meta['portswigger_topic']}",
                meta["subtitle"],
            ]
        ),
        "description": meta["subtitle"],
        "practice": False,
        "order_index": meta["number"],
    }


CHALLENGES = [_track_challenge(m) for m in TRACK_LABS] + PRACTICE_LABS


def sync_track_challenges() -> None:
    """Upsert track + practice labs (safe on every boot)."""
    for data in CHALLENGES:
        ch = Challenge.query.filter_by(slug=data["slug"]).first()
        if ch:
            for key, value in data.items():
                setattr(ch, key, value)
        else:
            db.session.add(Challenge(**data))
    db.session.commit()


def seed_if_empty() -> int:
    if not User.query.filter_by(username="demo").first():
        db.session.add(User(username="demo", password_hash=hash_password("demo123")))
        db.session.commit()
    sync_track_challenges()
    return Challenge.query.count()

"""Seed challenges and demo user. Run: python scripts/seed.py"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from sqli_lab import create_app
from sqli_lab.models import Challenge, User, db
from sqli_lab.auth_utils import hash_password

CHALLENGES = [
    {
        "slug": "error-based-intro",
        "title": "Practice: Error-based lookup",
        "sqli_type": "error-based",
        "difficulty": "easy",
        "points": 50,
        "flag": "FLAG{error_based_alpha}",
        "hints": json.dumps(["Try a single quote.", "Errors may reveal column names."]),
        "description": "Lookup a secret by ID. Extract FLAG{error_based_alpha} from lab_secrets.",
        "practice": True,
        "order_index": 1,
    },
    {
        "slug": "union-intro",
        "title": "Practice: UNION product search",
        "sqli_type": "union-based",
        "difficulty": "easy",
        "points": 60,
        "flag": "FLAG{union_product_leak}",
        "hints": json.dumps(["UNION SELECT needs matching columns.", "Probe column count with UNION SELECT NULL,..."]),
        "description": "Search products and leak hidden flag column via UNION.",
        "practice": True,
        "order_index": 2,
    },
    {
        "slug": "boolean-intro",
        "title": "Practice: Boolean blind profiles",
        "sqli_type": "boolean-blind",
        "difficulty": "medium",
        "points": 70,
        "flag": "FLAG{boolean_blind_bob}",
        "hints": json.dumps(["User bob exists.", "Use boolean conditions to infer bio content."]),
        "description": "Determine if profiles exist; extract bob's flag from bio.",
        "practice": True,
        "order_index": 3,
    },
    {
        "slug": "auth-bypass-intro",
        "title": "Practice: Auth bypass login",
        "sqli_type": "auth-bypass",
        "difficulty": "easy",
        "points": 80,
        "flag": "FLAG{auth_bypass_admin}",
        "hints": json.dumps(["Classic: admin' --", "Submit this flag after bypassing login."]),
        "description": "Bypass the vulnerable login without knowing the password. Flag: FLAG{auth_bypass_admin}",
        "practice": True,
        "order_index": 4,
    },
    {
        "slug": "time-based-intro",
        "title": "Practice: Time-based blind",
        "sqli_type": "time-based",
        "difficulty": "hard",
        "points": 90,
        "flag": "FLAG{time_based_carol}",
        "hints": json.dumps(["Measure response time.", "Flag documents: FLAG{time_based_carol}"]),
        "description": "Infer truth from delays when querying profiles. Submit FLAG{time_based_carol}.",
        "practice": True,
        "order_index": 5,
    },
    {
        "slug": "second-order-intro",
        "title": "Practice: Second-order injection",
        "sqli_type": "second-order",
        "difficulty": "medium",
        "points": 100,
        "flag": "FLAG{second_order_stored}",
        "hints": json.dumps(["Store payload first.", "Render step concatenates username."]),
        "description": "Store then trigger. Flag: FLAG{second_order_stored}",
        "practice": True,
        "order_index": 6,
    },
    # Challenge mode (catalog)
    {
        "slug": "error-based",
        "title": "Challenge: Error-based vault",
        "sqli_type": "error-based",
        "difficulty": "easy",
        "points": 100,
        "flag": "FLAG{error_based_alpha}",
        "hints": json.dumps(["ID 1 holds the flag.", "' OR '1'='1"]),
        "description": "Extract flag from lab_secrets via error-based SQLi.",
        "practice": False,
        "order_index": 10,
    },
    {
        "slug": "union-based",
        "title": "Challenge: UNION leak",
        "sqli_type": "union-based",
        "difficulty": "medium",
        "points": 120,
        "flag": "FLAG{union_product_leak}",
        "hints": json.dumps(["4 columns in lab_products.", "Third column can hold flag."]),
        "description": "UNION-based extraction from product search.",
        "practice": False,
        "order_index": 11,
    },
    {
        "slug": "boolean-blind",
        "title": "Challenge: Boolean blind",
        "sqli_type": "boolean-blind",
        "difficulty": "medium",
        "points": 130,
        "flag": "FLAG{boolean_blind_bob}",
        "hints": json.dumps(["Target user bob."]),
        "description": "Boolean blind inference on lab_profiles.",
        "practice": False,
        "order_index": 12,
    },
    {
        "slug": "time-based",
        "title": "Challenge: Time-based blind",
        "sqli_type": "time-based",
        "difficulty": "hard",
        "points": 150,
        "flag": "FLAG{time_based_carol}",
        "hints": json.dumps(["Watch elapsed_ms in response."]),
        "description": "Time-based blind on profile existence.",
        "practice": False,
        "order_index": 13,
    },
    {
        "slug": "auth-bypass",
        "title": "Challenge: Authentication bypass",
        "sqli_type": "auth-bypass",
        "difficulty": "easy",
        "points": 110,
        "flag": "FLAG{auth_bypass_admin}",
        "hints": json.dumps(["admin' --"]),
        "description": "Bypass login; flag FLAG{auth_bypass_admin}.",
        "practice": False,
        "order_index": 14,
    },
    {
        "slug": "second-order",
        "title": "Challenge: Second-order",
        "sqli_type": "second-order",
        "difficulty": "medium",
        "points": 140,
        "flag": "FLAG{second_order_stored}",
        "hints": json.dumps(["Two-step: store + render."]),
        "description": "Stored payload executed on render.",
        "practice": False,
        "order_index": 15,
    },
    {
        "slug": "stacked-queries",
        "title": "Challenge: Stacked queries (advanced)",
        "sqli_type": "stacked-queries",
        "difficulty": "hard",
        "points": 160,
        "flag": "FLAG{stacked_schema_peek}",
        "hints": json.dumps(["Enable advanced mode.", "Flag: FLAG{stacked_schema_peek}"]),
        "description": "Advanced gated stacked query demo. Enable advanced mode first.",
        "practice": False,
        "order_index": 16,
    },
    {
        "slug": "out-of-band",
        "title": "Challenge: Out-of-band (concept)",
        "sqli_type": "out-of-band",
        "difficulty": "medium",
        "points": 80,
        "flag": "FLAG{oob_concept_only}",
        "hints": json.dumps(["Read lesson — no live OOB channel.", "Flag in description."]),
        "description": "Concept-only. Submit FLAG{oob_concept_only} after completing the OOB lesson quiz.",
        "practice": False,
        "order_index": 17,
    },
]


def main():
    app = create_app()
    with app.app_context():
        for data in CHALLENGES:
            ch = Challenge.query.filter_by(slug=data["slug"]).first()
            if ch:
                for k, v in data.items():
                    setattr(ch, k, v)
            else:
                db.session.add(Challenge(**data))

        if not User.query.filter_by(username="demo").first():
            db.session.add(
                User(username="demo", password_hash=hash_password("demo123"))
            )

        db.session.commit()
        print(f"Seeded {len(CHALLENGES)} challenges and demo user (demo / demo123).")


if __name__ == "__main__":
    main()

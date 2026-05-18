"""Seed challenges and demo user. Run: python scripts/seed.py"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from sqli_lab import create_app
from sqli_lab.seed_db import seed_if_empty


def main():
    app = create_app()
    with app.app_context():
        count = seed_if_empty()
        print(f"Seeded {count} challenges and demo user (demo / demo123).")


if __name__ == "__main__":
    main()

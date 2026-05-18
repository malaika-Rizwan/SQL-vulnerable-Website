"""Reset lab tables (stacked-query advanced demos). Run: python scripts/reset_lab.py"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from sqli_lab.lab_db import init_lab_tables

if __name__ == "__main__":
    db_path = ROOT / "data" / "sqli_lab.db"
    if db_path.exists():
        db_path.unlink()
    init_lab_tables(str(db_path))
    print("Lab database reset at", db_path)

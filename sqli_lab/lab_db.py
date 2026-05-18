import sqlite3
from pathlib import Path


def get_lab_connection(db_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_lab_tables(db_path: str) -> None:
    conn = get_lab_connection(db_path)
    cur = conn.cursor()
    cur.executescript(
        """
        CREATE TABLE IF NOT EXISTS lab_secrets (
            id TEXT PRIMARY KEY,
            label TEXT NOT NULL,
            flag TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS lab_products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            flag TEXT
        );

        CREATE TABLE IF NOT EXISTS lab_users_vuln (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS lab_profiles (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            bio TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS lab_comments (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            body TEXT NOT NULL
        );
        """
    )
    conn.commit()

    cur.execute("SELECT COUNT(*) FROM lab_secrets")
    if cur.fetchone()[0] == 0:
        secrets = [
            ("1", "Alpha vault", "FLAG{error_based_alpha}"),
            ("2", "Beta vault", "FLAG{error_based_beta}"),
            ("3", "Gamma vault", "FLAG{union_gamma}"),
            ("hidden", "Shadow row", "FLAG{union_shadow}"),
        ]
        cur.executemany(
            "INSERT INTO lab_secrets (id, label, flag) VALUES (?, ?, ?)", secrets
        )

    cur.execute("SELECT COUNT(*) FROM lab_products")
    if cur.fetchone()[0] == 0:
        products = [
            (1, "Cyber Hoodie", 49.99, None),
            (2, "Neon Keyboard", 129.0, None),
            (3, "Debug Duck", 12.5, "FLAG{union_product_leak}"),
        ]
        cur.executemany(
            "INSERT INTO lab_products (id, name, price, flag) VALUES (?, ?, ?, ?)",
            products,
        )

    cur.execute("SELECT COUNT(*) FROM lab_users_vuln")
    if cur.fetchone()[0] == 0:
        users = [
            (1, "admin", "super_secret_admin_pass"),
            (2, "student", "learn123"),
            (3, "guest", "guest"),
        ]
        cur.executemany(
            "INSERT INTO lab_users_vuln (id, username, password) VALUES (?, ?, ?)", users
        )

    cur.execute("SELECT COUNT(*) FROM lab_profiles")
    if cur.fetchone()[0] == 0:
        profiles = [
            (1, "alice", "Security enthusiast."),
            (2, "bob", "FLAG{boolean_blind_bob}"),
            (3, "carol", "CTF player."),
        ]
        cur.executemany(
            "INSERT INTO lab_profiles (id, username, bio) VALUES (?, ?, ?)", profiles
        )

    conn.commit()
    conn.close()

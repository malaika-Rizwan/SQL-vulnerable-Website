"""
// VULNERABLE ON PURPOSE — EDUCATIONAL LAB ONLY
Each function mirrors a common SQLi pattern using sqlite3 string concatenation.
Fixed (safe) variants are provided alongside for defense training.
"""

import sqlite3
import time

from sqli_lab.lab_db import get_lab_connection


# --- Error-based -------------------------------------------------------------

def error_based_lookup(db_path: str, secret_id: str) -> dict:
    # VULNERABLE ON PURPOSE — EDUCATIONAL LAB ONLY
    conn = get_lab_connection(db_path)
    cur = conn.cursor()
    query = f"SELECT id, label, flag FROM lab_secrets WHERE id = '{secret_id}'"
    try:
        cur.execute(query)
        row = cur.fetchone()
        conn.close()
        if row:
            return {"ok": True, "data": dict(row), "query": query}
        return {"ok": True, "data": None, "query": query}
    except sqlite3.Error as exc:
        conn.close()
        return {"ok": False, "error": str(exc), "query": query}


def error_based_lookup_safe(db_path: str, secret_id: str) -> dict:
    conn = get_lab_connection(db_path)
    cur = conn.cursor()
    cur.execute("SELECT id, label, flag FROM lab_secrets WHERE id = ?", (secret_id,))
    row = cur.fetchone()
    conn.close()
    if row:
        return {"ok": True, "data": dict(row)}
    return {"ok": True, "data": None}


# --- Union-based -------------------------------------------------------------

def union_product_search(db_path: str, keyword: str) -> dict:
    # VULNERABLE ON PURPOSE — EDUCATIONAL LAB ONLY
    conn = get_lab_connection(db_path)
    cur = conn.cursor()
    query = (
        f"SELECT id, name, price, flag FROM lab_products "
        f"WHERE name LIKE '%{keyword}%'"
    )
    try:
        cur.execute(query)
        rows = [dict(r) for r in cur.fetchall()]
        conn.close()
        return {"ok": True, "rows": rows, "query": query}
    except sqlite3.Error as exc:
        conn.close()
        return {"ok": False, "error": str(exc), "query": query}


def union_product_search_safe(db_path: str, keyword: str) -> dict:
    conn = get_lab_connection(db_path)
    cur = conn.cursor()
    cur.execute(
        "SELECT id, name, price, flag FROM lab_products WHERE name LIKE ?",
        (f"%{keyword}%",),
    )
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return {"ok": True, "rows": rows}


# --- Boolean blind -----------------------------------------------------------

def boolean_profile_exists(db_path: str, username: str) -> dict:
    # VULNERABLE ON PURPOSE — EDUCATIONAL LAB ONLY
    conn = get_lab_connection(db_path)
    cur = conn.cursor()
    query = f"SELECT bio FROM lab_profiles WHERE username = '{username}'"
    try:
        cur.execute(query)
        row = cur.fetchone()
        conn.close()
        exists = row is not None
        return {"ok": True, "exists": exists, "hint": "Profile found." if exists else "No profile.", "query": query}
    except sqlite3.Error as exc:
        conn.close()
        return {"ok": False, "error": str(exc), "query": query}


def boolean_profile_exists_safe(db_path: str, username: str) -> dict:
    conn = get_lab_connection(db_path)
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM lab_profiles WHERE username = ? LIMIT 1", (username,))
    exists = cur.fetchone() is not None
    conn.close()
    return {"ok": True, "exists": exists}


# --- Time-based blind --------------------------------------------------------

def time_based_check(db_path: str, username: str) -> dict:
    # VULNERABLE ON PURPOSE — EDUCATIONAL LAB ONLY
    # SQLite delay via heavy LIKE on randomblob when condition is true.
    conn = get_lab_connection(db_path)
    cur = conn.cursor()
    query = (
        f"SELECT CASE WHEN (SELECT COUNT(*) FROM lab_profiles WHERE username = '{username}') "
        f"THEN (SELECT COUNT(*) FROM lab_profiles, lab_profiles, lab_profiles) ELSE 0 END"
    )
    start = time.perf_counter()
    try:
        cur.execute(query)
        cur.fetchone()
        elapsed = time.perf_counter() - start
        conn.close()
        return {"ok": True, "elapsed_ms": int(elapsed * 1000), "query": query}
    except sqlite3.Error as exc:
        conn.close()
        return {"ok": False, "error": str(exc), "query": query}


# --- Auth bypass -------------------------------------------------------------

def auth_bypass_login(db_path: str, username: str, password: str) -> dict:
    # VULNERABLE ON PURPOSE — EDUCATIONAL LAB ONLY
    conn = get_lab_connection(db_path)
    cur = conn.cursor()
    query = (
        f"SELECT id, username FROM lab_users_vuln "
        f"WHERE username = '{username}' AND password = '{password}'"
    )
    try:
        cur.execute(query)
        row = cur.fetchone()
        conn.close()
        if row:
            return {"ok": True, "authenticated": True, "user": dict(row), "query": query}
        return {"ok": True, "authenticated": False, "query": query}
    except sqlite3.Error as exc:
        conn.close()
        return {"ok": False, "error": str(exc), "query": query}


def auth_bypass_login_safe(db_path: str, username: str, password: str) -> dict:
    conn = get_lab_connection(db_path)
    cur = conn.cursor()
    cur.execute(
        "SELECT id, username FROM lab_users_vuln WHERE username = ? AND password = ?",
        (username, password),
    )
    row = cur.fetchone()
    conn.close()
    if row:
        return {"ok": True, "authenticated": True, "user": dict(row)}
    return {"ok": True, "authenticated": False}


# --- Second-order ------------------------------------------------------------

def second_order_store_comment(db_path: str, username: str, body: str) -> dict:
    conn = get_lab_connection(db_path)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO lab_comments (username, body) VALUES (?, ?)", (username, body)
    )
    conn.commit()
    conn.close()
    return {"ok": True, "stored": True}


def second_order_render(db_path: str, username: str) -> dict:
    # VULNERABLE ON PURPOSE — EDUCATIONAL LAB ONLY (stored payload executed later)
    conn = get_lab_connection(db_path)
    cur = conn.cursor()
    query = f"SELECT id, username, body FROM lab_comments WHERE username = '{username}'"
    try:
        cur.execute(query)
        rows = [dict(r) for r in cur.fetchall()]
        conn.close()
        return {"ok": True, "rows": rows, "query": query}
    except sqlite3.Error as exc:
        conn.close()
        return {"ok": False, "error": str(exc), "query": query}


# --- Stacked (advanced) ------------------------------------------------------

def stacked_multi_statement(db_path: str, table_name: str, advanced_unlocked: bool) -> dict:
    if not advanced_unlocked:
        return {"ok": False, "error": "Advanced mode required. Enable on challenge page."}
    # VULNERABLE ON PURPOSE — EDUCATIONAL LAB ONLY
    conn = get_lab_connection(db_path)
    cur = conn.cursor()
    query = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'"
    try:
        cur.executescript(
            f"{query}; SELECT sql FROM sqlite_master WHERE name='lab_secrets';"
        )
        rows = cur.fetchall()
        conn.close()
        return {"ok": True, "rows": [str(r) for r in rows], "query": query}
    except sqlite3.Error as exc:
        conn.close()
        return {"ok": False, "error": str(exc), "query": query}

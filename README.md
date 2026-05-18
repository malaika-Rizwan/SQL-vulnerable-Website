# SQLi Lab — Python + HTML + CSS

Educational SQL injection training lab. **Python (Flask)** backend, **HTML (Jinja2)** templates, **CSS** styling. No React, no Next.js, no Node frontend.

> **EDUCATIONAL USE ONLY** — Run on localhost or a supervised class VM. Do not deploy publicly.

## Project structure

```
sqli.task/
├── run.py              # Start the server
├── start.bat           # Windows one-click start
├── requirements.txt    # Python dependencies
├── sqli_lab/           # Flask app (routes, models, vuln labs)
├── templates/          # HTML pages
├── static/css/         # Stylesheets
├── scripts/seed.py     # Database seed
└── tests/              # pytest
```

## Quick start (Windows)

1. Install [Python 3.11+](https://www.python.org/downloads/) and enable **Add to PATH**.
2. Double-click **`start.bat`** or run:

```bash
cd d:\sqli.task
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python scripts\seed.py
python run.py
```

3. Open **http://localhost:5000** (not port 3000).

**Demo account:** `demo` / `demo123`

## Routes

| URL | Page |
|-----|------|
| `/` | Home + disclaimer |
| `/login`, `/register` | Authentication |
| `/dashboard` | Learn · Practice · Challenges |
| `/learn` | SQLi lessons + quizzes |
| `/practice` | Guided vulnerable labs |
| `/challenges` | Solve challenges one-by-one |
| `/leaderboard` | Scoring board |

## Docker

```bash
docker compose up --build
```

→ http://localhost:5000

## Tests

```bash
pytest
```

## Reset data

```bash
del data\sqli_lab.db
python scripts\seed.py
```

## Tech stack

- **Flask** — web server and routing
- **Jinja2** — HTML templates
- **CSS** — `static/css/style.css`
- **SQLite** — app data + intentionally vulnerable lab tables
- **bcrypt** — password hashing

Vulnerable SQL lives only in `sqli_lab/vuln/queries.py` (labeled *EDUCATIONAL LAB ONLY*).

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

## Deploy on Vercel

1. Import repo [SQL-vulnerable-Website](https://github.com/malaika-Rizwan/SQL-vulnerable-Website) on Vercel.
2. Framework preset: **Other** (Python is auto-detected via `app.py`).
3. Add environment variable:
   - `FLASK_SECRET_KEY` = long random string (required)
4. Add **`FLASK_SECRET_KEY`** (required) in Project → Settings → Environment Variables.
5. Deploy (do **not** add a custom `vercel.json` — Vercel auto-detects Flask via `app.py`).

Entrypoint: `app.py` exports `app`. Static CSS is served from `public/css/`.

> **Note:** Vercel uses ephemeral `/tmp` storage — progress resets on cold starts. This lab is intended for **local/class use**; Vercel is optional for demos only.

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

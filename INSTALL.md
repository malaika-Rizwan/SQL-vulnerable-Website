# Install Python (required)

Your terminal shows **Python was not found**. The app is Python-only; you must install Python first.

## Step 1 — Turn off the fake Python shortcut

1. Open **Settings** → **Apps** → **Advanced app settings** → **App execution aliases**
2. Turn **OFF** both:
   - `python.exe`
   - `python3.exe`

(Those point to the Microsoft Store and block the real Python.)

## Step 2 — Install Python 3.12

**Option A — Website (recommended)**

1. Go to https://www.python.org/downloads/
2. Download **Python 3.12**
3. Run the installer
4. Check **“Add python.exe to PATH”** at the bottom
5. Click **Install Now**

**Option B — Command (PowerShell as Admin)**

```powershell
winget install -e --id Python.Python.3.12
```

Close and reopen your terminal after install.

## Step 3 — Verify

In **Git Bash** or **CMD**:

```bash
python --version
```

You should see `Python 3.12.x` (not “Microsoft Store”).

## Step 4 — Run SQLi Lab (Git Bash)

Use **forward slashes** in Git Bash:

```bash
cd /d/sqli.task
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
python scripts/seed.py
python run.py
```

Then open: **http://localhost:5000**  
Login: `demo` / `demo123`

## Step 4 — Run SQLi Lab (CMD / double-click)

Double-click **`start.bat`** in the project folder.

---

### Common mistakes

| Wrong | Right |
|-------|--------|
| `.venv\Scripts\activate` in Git Bash | `source .venv/Scripts/activate` |
| `http://localhost:3000` | `http://localhost:5000` |
| `npm run dev` | `python run.py` |

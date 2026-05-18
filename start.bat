@echo off
cd /d "%~dp0"
echo SQLi Lab - Python/Flask (port 5000)
echo.

set "PY=python"
where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
  if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" (
    set "PY=%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
  ) else (
    echo Python not found. See INSTALL.md
    pause
    exit /b 1
  )
)

if not exist ".venv\Scripts\python.exe" (
  echo Creating virtual environment...
  "%PY%" -m venv .venv
)

call .venv\Scripts\activate.bat
pip install -r requirements.txt -q
if not exist "data\sqli_lab.db" (
  "%PY%" scripts\seed.py
)
echo.
echo Open http://localhost:5000
echo Demo login: demo / demo123
echo.
.venv\Scripts\python.exe run.py

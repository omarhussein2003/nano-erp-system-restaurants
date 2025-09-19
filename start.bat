@echo off
setlocal enabledelayedexpansion

cd /d "%~dp0"

if exist .venv rmdir /s /q .venv
echo Creating fresh virtual environment...
py -3 -m venv .venv

call .venv\Scripts\activate.bat
echo Installing dependencies...
python -m pip install --upgrade pip >NUL 2>&1
pip install -r requirements.txt

echo Testing imports...
python -c "import app.models; print('✓ Models OK')"
python -c "import app.main; print('✓ App OK')"

echo Starting server on http://127.0.0.1:8000
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

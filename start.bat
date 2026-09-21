@echo off
REM Tharros - mode production local : compile le front puis lance l'API qui sert tout sur http://localhost:8000
cd /d "%~dp0"
REM Libere les ports d'un lancement precedent (processus orphelins)
call "%~dp0stop.bat" >nul
set "PATH=%~dp0.tools\node;%PATH%"
if not exist backend\.venv\Scripts\python.exe (
  python -m pip install -q virtualenv
  python -m virtualenv -q --always-copy backend\.venv
  backend\.venv\Scripts\python.exe -m pip install -q -r backend\requirements.txt
)
if not exist frontend\node_modules ( cd frontend && call npm install --no-audit --no-fund && cd .. )
cd frontend && call npm run build && cd ..
echo.
echo Site : http://localhost:8000     Admin : http://localhost:8000/admin
start "" http://localhost:8000/
cd backend && .venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000

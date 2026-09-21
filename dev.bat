@echo off
REM Tharros - mode developpement : API (rechargement auto) + front Vite (rechargement a chaud)
REM Site : http://localhost:5173   Admin : http://localhost:5173/admin   API docs : http://localhost:8000/api/docs
cd /d "%~dp0"
REM Libere les ports d'un lancement precedent (processus orphelins)
call "%~dp0stop.bat" >nul
set "PATH=%~dp0.tools\node;%PATH%"
if not exist backend\.venv\Scripts\python.exe (
  echo Creation de l'environnement Python...
  python -m pip install -q virtualenv
  python -m virtualenv -q --always-copy backend\.venv
  backend\.venv\Scripts\python.exe -m pip install -q -r backend\requirements.txt
)
if not exist frontend\node_modules (
  echo Installation des dependances front...
  cd frontend && call npm install --no-audit --no-fund && cd ..
)
start "Tharros API" cmd /k "cd /d "%~dp0backend" && .venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000"
start "Tharros Front" cmd /k "cd /d "%~dp0frontend" && set "PATH=%~dp0.tools\node;%PATH%" && npm run dev"
timeout /t 4 >nul
start "" http://localhost:5173/

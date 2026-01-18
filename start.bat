@echo off
REM Script de démarrage du Threat Analyzer

echo.
echo ===================================
echo  Threat Analyzer - Démarrage
echo ===================================
echo.

REM Vérifier Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERREUR] Python n'est pas installé ou pas dans le PATH
    pause
    exit /b 1
)

REM Vérifier Node.js
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERREUR] Node.js n'est pas installé ou pas dans le PATH
    pause
    exit /b 1
)

echo [OK] Python et Node.js détectés

REM Ouvrir deux terminals pour backend et frontend
echo.
echo Démarrage du backend...
start cmd /k "cd threat-analyzer-backend && python -m pip install -q fastapi uvicorn python-multipart chromadb sentence-transformers pandas pypdf python-dotenv anthropic requests 2>nul && uvicorn main:app --reload --port 8000"

timeout /t 3 /nobreak

echo Démarrage du frontend...
start cmd /k "cd threat-analyzer-front && npm install >nul 2>&1 && npm run dev"

echo.
echo ===================================
echo Démarrage en cours...
echo Backend: http://localhost:8000
echo Frontend: http://localhost:5173
echo ===================================
echo.

@echo off
echo === Preparation du commit ===
cd /d "%~dp0"

REM Supprimer le fichier de verrou s'il existe
if exist .git\index.lock del /f .git\index.lock

echo Ajout des fichiers backend...
git add threat-analyzer-backend\main.py
git add threat-analyzer-backend\rag\
git add threat-analyzer-backend\services\
git add threat-analyzer-backend\parsers\
git add threat-analyzer-backend\requirements.txt
git add threat-analyzer-backend\test_system.py
git add threat-analyzer-backend\.env.example
git add threat-analyzer-backend\CREATE_TABLES.sql
git add threat-analyzer-backend\init_tables.py
git add threat-analyzer-backend\CONFIGURATION_MYSQL.md
git add threat-analyzer-backend\GUIDE_CREATION_TABLES.md

echo Ajout des fichiers frontend...
git add threat-analyzer-front\src\
git add threat-analyzer-front\package.json
git add threat-analyzer-front\package-lock.json

echo Ajout de la documentation...
git add DOCUMENT_FINAL_MISE_A_JOUR.md
git add DOCUMENT_COMPLET_MISE_A_JOUR.md
git add AMELIORATIONS_IMPLEMENTEES.md
git add ETAT_IMPLEMENTATION.md
git add RAPPORT_TEST_SYSTEME.md
git add start-backend.ps1
git add commit-and-push.ps1
git add .gitignore

echo.
echo === Statut des fichiers ===
git status --short

echo.
echo === Creation du commit ===
git commit -m "feat: Ajout des fonctionnalites avancees et mise a jour documentation

- Ajout des services d'enrichissement (MITRE, NVD, Standards)
- Implementation des parseurs C4 et UML (testes et fonctionnels)
- Ajout des metriques de validation (precision, rappel, F1-score)
- Systeme d'authentification utilisateur complet
- Tests systeme automatises (93.5%% de reussite - 29/31 tests)
- Mise a jour complete de la documentation
- Amelioration de l'explicabilite avec scores de confiance
- Enrichissement multi-sources (CWE, CVSS, MITRE, OWASP, CVE)
- Comparaison avec standards (OWASP, CIS Controls, NIST CSF)
- Stockage persistant avec SQLite
- Interface utilisateur amelioree avec nouveaux composants"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo === Commit reussi! ===
    echo.
    set /p push="Voulez-vous pousser vers GitHub? (O/N): "
    if /i "%push%"=="O" (
        echo.
        echo === Push vers GitHub ===
        git push origin main
        if %ERRORLEVEL% EQU 0 (
            echo.
            echo === Push reussi! ===
        ) else (
            echo.
            echo === Erreur lors du push ===
        )
    )
) else (
    echo.
    echo === Erreur lors du commit ===
)

pause

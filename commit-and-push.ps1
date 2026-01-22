# Script pour faire le commit et push vers GitHub
# Exécuter ce script dans PowerShell

Write-Host "=== Préparation du commit ===" -ForegroundColor Cyan

# Aller dans le répertoire du projet
cd $PSScriptRoot

# Supprimer le fichier de verrou s'il existe
if (Test-Path .git\index.lock) {
    Write-Host "Suppression du fichier de verrou..." -ForegroundColor Yellow
    Remove-Item .git\index.lock -Force
}

# Ajouter les fichiers modifiés et nouveaux (sauf les fichiers sensibles)
Write-Host "`nAjout des fichiers backend..." -ForegroundColor Green
git add threat-analyzer-backend/main.py
git add threat-analyzer-backend/rag/
git add threat-analyzer-backend/services/
git add threat-analyzer-backend/parsers/
git add threat-analyzer-backend/requirements.txt
git add threat-analyzer-backend/test_system.py
git add threat-analyzer-backend/.env.example
git add threat-analyzer-backend/CREATE_TABLES.sql
git add threat-analyzer-backend/init_tables.py
git add threat-analyzer-backend/CONFIGURATION_MYSQL.md
git add threat-analyzer-backend/GUIDE_CREATION_TABLES.md

Write-Host "Ajout des fichiers frontend..." -ForegroundColor Green
git add threat-analyzer-front/src/
git add threat-analyzer-front/package.json
git add threat-analyzer-front/package-lock.json

Write-Host "Ajout de la documentation..." -ForegroundColor Green
git add DOCUMENT_FINAL_MISE_A_JOUR.md
git add DOCUMENT_COMPLET_MISE_A_JOUR.md
git add AMELIORATIONS_IMPLEMENTEES.md
git add ETAT_IMPLEMENTATION.md
git add RAPPORT_TEST_SYSTEME.md
git add start-backend.ps1

# Vérifier le statut
Write-Host "`n=== Statut des fichiers à commiter ===" -ForegroundColor Cyan
git status --short

# Demander confirmation
Write-Host "`n=== Confirmation ===" -ForegroundColor Yellow
$confirmation = Read-Host "Voulez-vous continuer avec le commit? (O/N)"
if ($confirmation -ne "O" -and $confirmation -ne "o") {
    Write-Host "Commit annulé." -ForegroundColor Red
    exit
}

# Faire le commit
Write-Host "`n=== Création du commit ===" -ForegroundColor Cyan
$commitMessage = @"
feat: Ajout des fonctionnalités avancées et mise à jour documentation

- Ajout des services d'enrichissement (MITRE, NVD, Standards)
- Implémentation des parseurs C4 et UML (testés et fonctionnels)
- Ajout des métriques de validation (précision, rappel, F1-score)
- Système d'authentification utilisateur complet
- Tests système automatisés (93.5% de réussite - 29/31 tests)
- Mise à jour complète de la documentation
- Amélioration de l'explicabilité avec scores de confiance
- Enrichissement multi-sources (CWE, CVSS, MITRE, OWASP, CVE)
- Comparaison avec standards (OWASP, CIS Controls, NIST CSF)
- Stockage persistant avec SQLite
- Interface utilisateur améliorée avec nouveaux composants
"@

git commit -m $commitMessage

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n=== Commit réussi! ===" -ForegroundColor Green
    
    # Demander si on veut push
    $pushConfirmation = Read-Host "`nVoulez-vous pousser vers GitHub? (O/N)"
    if ($pushConfirmation -eq "O" -or $pushConfirmation -eq "o") {
        Write-Host "`n=== Push vers GitHub ===" -ForegroundColor Cyan
        git push origin main
        if ($LASTEXITCODE -eq 0) {
            Write-Host "`n=== Push réussi! ===" -ForegroundColor Green
        } else {
            Write-Host "`n=== Erreur lors du push ===" -ForegroundColor Red
        }
    }
} else {
    Write-Host "`n=== Erreur lors du commit ===" -ForegroundColor Red
    Write-Host "Vérifiez les messages d'erreur ci-dessus." -ForegroundColor Yellow
}

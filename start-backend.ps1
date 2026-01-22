# Script PowerShell pour démarrer le backend Threat Analyzer

Write-Host ""
Write-Host "===================================" -ForegroundColor Cyan
Write-Host "  Démarrage du Backend" -ForegroundColor Cyan
Write-Host "===================================" -ForegroundColor Cyan
Write-Host ""

# Vérifier Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[OK] Python détecté: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERREUR] Python n'est pas installé ou pas dans le PATH" -ForegroundColor Red
    Write-Host "Appuyez sur une touche pour quitter..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

# Aller dans le dossier backend
$backendPath = Join-Path $PSScriptRoot "threat-analyzer-backend"
Set-Location $backendPath

# Vérifier que le dossier existe
if (-not (Test-Path "main.py")) {
    Write-Host "[ERREUR] Le fichier main.py n'existe pas dans threat-analyzer-backend" -ForegroundColor Red
    Write-Host "Assurez-vous d'exécuter ce script depuis la racine du projet" -ForegroundColor Yellow
    Write-Host "Appuyez sur une touche pour quitter..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

Write-Host "[INFO] Installation des dépendances Python..." -ForegroundColor Yellow
if (Test-Path "requirements.txt") {
    python -m pip install -q -r requirements.txt 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ATTENTION] Certaines dépendances peuvent manquer. Installation manuelle recommandée." -ForegroundColor Yellow
        Write-Host "[INFO] Exécutez: pip install -r requirements.txt" -ForegroundColor Yellow
    } else {
        Write-Host "[OK] Dépendances installées" -ForegroundColor Green
    }
} else {
    Write-Host "[ATTENTION] Fichier requirements.txt non trouvé" -ForegroundColor Yellow
}
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ATTENTION] Certaines dépendances peuvent manquer. Installation manuelle recommandée." -ForegroundColor Yellow
    Write-Host "[INFO] Exécutez: pip install -r requirements.txt" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "[INFO] Démarrage du serveur backend sur http://localhost:8000" -ForegroundColor Green
Write-Host "[INFO] Appuyez sur Ctrl+C pour arrêter le serveur" -ForegroundColor Yellow
Write-Host ""

# Démarrer uvicorn
python -m uvicorn main:app --reload --port 8000

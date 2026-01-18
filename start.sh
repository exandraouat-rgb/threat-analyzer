#!/bin/bash
# Script de démarrage du Threat Analyzer (Linux/Mac)

echo ""
echo "==================================="
echo " Threat Analyzer - Démarrage"
echo "==================================="
echo ""

# Vérifier Python
if ! command -v python3 &> /dev/null; then
    echo "[ERREUR] Python 3 n'est pas installé"
    exit 1
fi

# Vérifier Node.js
if ! command -v node &> /dev/null; then
    echo "[ERREUR] Node.js n'est pas installé"
    exit 1
fi

echo "[OK] Python et Node.js détectés"
echo ""

# Installer dépendances backend
echo "Installation des dépendances Python..."
cd threat-analyzer-backend
pip3 install -q fastapi uvicorn python-multipart chromadb sentence-transformers pandas pypdf python-dotenv anthropic requests 2>/dev/null

# Démarrer backend en background
echo "Démarrage du backend..."
python3 -m uvicorn main:app --reload --port 8000 &
BACKEND_PID=$!
sleep 3

# Démarrer frontend
echo "Démarrage du frontend..."
cd ../threat-analyzer-front
npm install > /dev/null 2>&1
npm run dev

# Nettoyage
kill $BACKEND_PID 2>/dev/null

echo ""
echo "==================================="
echo "Application fermée"
echo "==================================="

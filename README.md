# Threat Analyzer - Guide de Démarrage

## Prérequis
- Python 3.8+
- Node.js 16+
- npm ou yarn

## Installation

### Backend

```bash
cd threat-analyzer-backend

# Installer les dépendances
pip install fastapi uvicorn python-multipart chromadb sentence-transformers pandas pypdf python-dotenv anthropic requests

# Vérifier le fichier .env (ANTHROPIC_API_KEY doit être configuré)
cat .env
```

### Frontend

```bash
cd threat-analyzer-front

# Installer les dépendances
npm install
```

## Démarrage

### 1. Démarrer le Backend

```bash
cd threat-analyzer-backend
uvicorn main:app --reload --port 8000
```

Le backend devrait être accessible à `http://localhost:8000`

Vérifier le health check: `curl http://localhost:8000/health`

### 2. Démarrer le Frontend

```bash
cd threat-analyzer-front
npm run dev
```

Le frontend devrait être accessible à `http://localhost:5173`

## Utilisation

1. Aller à `http://localhost:5173`
2. Remplir le formulaire:
   - Nom du projet
   - Type d'application
   - Description de l'architecture
   - (Optionnel) Fichier PDF ou JSON
3. Cliquer sur "Analyser"
4. Les résultats s'affichent avec:
   - Score de risque
   - Liste des menaces détectées
   - Bouton de téléchargement PDF

## Dépannage

### Le frontend affiche une erreur
- Vérifier que le backend est lancé: `curl http://localhost:8000/health`
- Vérifier la console du navigateur (F12) pour les erreurs
- Vérifier que le port 8000 n'est pas utilisé par un autre service

### Le backend crashe
- Vérifier que `Données.csv` existe
- Vérifier que la clé API Anthropic est configurée dans `.env`
- Consulter les logs du terminal

### Les dépendances ne s'installent pas
- Assurez-vous que pip est à jour: `pip install --upgrade pip`
- Essayer avec: `pip install --user -r requirements.txt` (si file existe)

## Structure du Projet

```
threat-analyzer-backend/
├── main.py              # Serveur FastAPI
├── Données.csv         # Base de données des menaces
├── .env                # Configuration (clé API)
├── rag/
│   ├── build_kb.py     # Construction base vectorielle
│   └── query_kb.py     # Recherche RAG
└── services/
    ├── llm_service.py           # Analyse avec Claude
    ├── risk_score_service.py    # Calcul scores
    ├── dashboard_adapter.py     # Formatage résultats
    └── pdf_report_service.py    # Génération PDF

threat-analyzer-front/
├── src/
│   ├── App.tsx         # Composant principal
│   ├── config.ts       # Configuration API
│   └── main.tsx        # Point d'entrée
├── vite.config.ts      # Configuration Vite
└── package.json        # Dépendances npm
```

## API Endpoints

- `GET /health` - Vérifier l'état du serveur
- `POST /analyze` - Analyser un projet
  - Paramètres: project_name, app_type, architecture_description, file (optionnel)
- `POST /generate-pdf` - Générer le rapport PDF

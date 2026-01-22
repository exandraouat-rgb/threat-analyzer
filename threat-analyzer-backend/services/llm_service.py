import os
import json
from anthropic import Anthropic
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

client = Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

def analyze_with_claude(rag_context: str, user_input: str) -> dict:
    """
    Analyse de menaces basée sur un RAG
    Retourne TOUJOURS un dictionnaire Python
    """

    prompt = f"""
Tu es un expert senior en cybersécurité spécialisé en modélisation des menaces applicatives.

MENACES POTENTIELLES (extraits du CSV - certaines peuvent ne pas être pertinentes) :
{rag_context}

DESCRIPTION DU PROJET :
{user_input}

FORMAT STRICT JSON (OBLIGATOIRE) :
{{
  "niveau_global": "Faible | Élevé | Critique",
  "menaces": [
    {{
      "nom": "Nom de la menace (ex: SQL Injection)",
      "gravite": "Critique | Élevée | Moyenne | Faible",
      "description": "Description détaillée de la menace et de son impact",
      "recommandations": [
        "Recommandation 1 détaillée et actionnable",
        "Recommandation 2 détaillée et actionnable",
        "Recommandation 3 détaillée et actionnable"
      ],
      "cwe_id": "CWE-XXX (extrait du contexte RAG si disponible)",
      "cvss_score": "X.X (extrait du contexte RAG si disponible)",
      "mitre_attack_id": "TXXXX (extrait du contexte RAG si disponible)",
      "owasp_category": "AXX:YYYY (extrait du contexte RAG si disponible)",
      "score_confiance": 0.85
    }}
  ]
}}

IMPORTANT pour les métadonnées :
- Extrais CWE ID, CVSS Score, MITRE ATT&CK ID, OWASP Category directement du contexte RAG
- Si non disponible, utilise "N/A"
- score_confiance : nombre entre 0.0 et 1.0 indiquant ta certitude (0.9+ = très sûr, 0.7-0.9 = assez sûr, <0.7 = moins sûr)

RÈGLES CRITIQUES DE FILTRAGE :
1. **FILTRAGE PAR TYPE D'APPLICATION** : Tu DOIS ignorer complètement les menaces qui ne sont PAS pertinentes pour le type d'application spécifié :
   - Si c'est une APPLICATION MOBILE (iOS/Android) : IGNORE toutes les menaces spécifiques aux applications WEB (SQL Injection, XSS web, serveurs web, etc.)
   - Si c'est une APPLICATION WEB : IGNORE les menaces spécifiques aux applications mobiles (Keychain, EncryptedSharedPreferences, certificate pinning mobile, etc.)
   - Si c'est une API : IGNORE les menaces spécifiques aux interfaces utilisateur web ou mobiles
   - Ne garde QUE les menaces dont l'architecture_description correspond au type d'application

2. **EXTRACTION DES RECOMMANDATIONS** : Extrais les recommandations directement des champs "Recommandation de mitigation" du contexte RAG
3. **SÉPARATION DES RECOMMANDATIONS** : Si plusieurs recommandations sont présentes, sépare-les en éléments distincts du tableau
4. **QUALITÉ DES RECOMMANDATIONS** : Chaque recommandation doit être claire, actionnable et spécifique
5. **GRAVITÉ** : Utilise la gravité exacte du CSV (Critique, HAUTE, MOYENNE, Faible) - normalise HAUTE en "Élevée"
6. **FORMAT** : Aucune phrase hors JSON, aucun markdown, réponds uniquement avec un JSON valide

EXEMPLE : Si le type d'application est "mobile" et qu'une menace parle de "Application web avec authentification utilisateur et base de données MySQL", IGNORE cette menace car elle n'est pas pertinente pour une application mobile.
"""

    response = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=4000,
        messages=[{"role": "user", "content": prompt}]
    )

    raw_text = response.content[0].text.strip()

    if not raw_text:
        return {"error": "Réponse vide du modèle"}

    try:
        return json.loads(raw_text)
    except json.JSONDecodeError:
        return {
            "error": "JSON invalide retourné par Claude",
            "raw_response": raw_text
        }

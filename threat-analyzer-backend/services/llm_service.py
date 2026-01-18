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

MENACES PERTINENTES :
{rag_context}

DESCRIPTION DU PROJET :
{user_input}

FORMAT STRICT JSON (OBLIGATOIRE) :
{{
  "niveau_global": "Faible | Élevé | Critique",
  "menaces": [
    {{
      "nom": "",
      "gravite": "",
      "description": "",
      "recommandations": []
    }}
  ]
}}

RÈGLES :
- Aucune phrase hors JSON
- Aucun markdown
- Réponds uniquement avec un JSON valide
"""

    response = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=1000,
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

"""
Service utilisant LangChain pour orchestrer l'analyse IA
Améliore la gestion des prompts et des chaînes de traitement
"""
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import json
import os
from dotenv import load_dotenv

load_dotenv()

def create_threat_analysis_chain():
    """
    Crée une chaîne LangChain pour l'analyse de menaces
    """
    llm = ChatAnthropic(
        model="claude-3-haiku-20240307",
        temperature=0.1,
        max_tokens=4000,
        api_key=os.getenv("ANTHROPIC_API_KEY")
    )
    
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", """Tu es un expert senior en cybersécurité spécialisé en modélisation des menaces applicatives.
        
RÈGLES CRITIQUES DE FILTRAGE :
1. **FILTRAGE PAR TYPE D'APPLICATION** : Tu DOIS ignorer complètement les menaces qui ne sont PAS pertinentes pour le type d'application spécifié.
2. **EXTRACTION DES RECOMMANDATIONS** : Extrais les recommandations directement des champs "Recommandation de mitigation" du contexte RAG.
3. **QUALITÉ** : Chaque recommandation doit être claire, actionnable et spécifique.
4. **FORMAT** : Réponds uniquement avec un JSON valide, aucune phrase hors JSON."""),
        ("human", """MENACES POTENTIELLES (extraits du CSV) :
{rag_context}

DESCRIPTION DU PROJET :
{user_input}

FORMAT STRICT JSON (OBLIGATOIRE) :
{{
  "niveau_global": "Faible | Élevé | Critique",
  "menaces": [
    {{
      "nom": "Nom de la menace",
      "gravite": "Critique | Élevée | Moyenne | Faible",
      "description": "Description détaillée",
      "recommandations": ["Rec 1", "Rec 2"],
      "cwe_id": "CWE-XXX",
      "cvss_score": "X.X",
      "mitre_attack_id": "TXXXX",
      "owasp_category": "AXX:YYYY",
      "score_confiance": 0.85
    }}
  ]
}}""")
    ])
    
    output_parser = StrOutputParser()
    
    chain = (
        {"rag_context": RunnablePassthrough(), "user_input": RunnablePassthrough()}
        | prompt_template
        | llm
        | output_parser
    )
    
    return chain

def analyze_with_langchain(rag_context: str, user_input: str) -> dict:
    """
    Analyse de menaces utilisant LangChain pour l'orchestration
    """
    try:
        chain = create_threat_analysis_chain()
        
        result = chain.invoke({
            "rag_context": rag_context,
            "user_input": user_input
        })
        
        # Parser le JSON
        result = result.strip()
        
        # Nettoyer le résultat (enlever markdown si présent)
        if result.startswith("```json"):
            result = result[7:]
        if result.startswith("```"):
            result = result[3:]
        if result.endswith("```"):
            result = result[:-3]
        result = result.strip()
        
        return json.loads(result)
    except json.JSONDecodeError as e:
        return {
            "error": "JSON invalide retourné par le modèle",
            "raw_response": result if 'result' in locals() else ""
        }
    except Exception as e:
        return {
            "error": f"Erreur lors de l'analyse: {str(e)}"
        }

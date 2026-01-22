import pandas as pd
import chromadb
from sentence_transformers import SentenceTransformer

def build_vector_db(csv_path: str):
    df = pd.read_csv(csv_path)

    model = SentenceTransformer("all-MiniLM-L6-v2")
    client = chromadb.Client()

    collection = client.create_collection(name="threats")

    for i, row in df.iterrows():
        text = f"""
Architecture: {row.get('architecture_description', '')}
Type de menace: {row.get('threat_type', '')}
Gravité: {row.get('severity', '')}
Description: {row.get('threat_description', '')}
Impact: {row.get('impact', '')}
Vecteur d'attaque: {row.get('attack_vector', '')}
Recommandation de mitigation: {row.get('mitigation_recommendation', '')}
CWE ID: {row.get('cwe_id', '')}
CVSS Score: {row.get('cvss_score', '')}
MITRE ATT&CK: {row.get('mitre_attack_id', '')}
OWASP Category: {row.get('owasp_category', '')}
"""
        embedding = model.encode(text).tolist()

        collection.add(
            documents=[text],
            embeddings=[embedding],
            ids=[str(i)]
        )

    return collection

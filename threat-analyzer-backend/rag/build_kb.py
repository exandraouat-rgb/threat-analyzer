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
Menace: {row.get('menace', '')}
Description: {row.get('description', '')}
Impact: {row.get('impact', '')}
Solution: {row.get('solution', '')}
"""
        embedding = model.encode(text).tolist()

        collection.add(
            documents=[text],
            embeddings=[embedding],
            ids=[str(i)]
        )

    return collection

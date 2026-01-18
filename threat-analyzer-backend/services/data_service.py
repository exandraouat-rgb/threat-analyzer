import pandas as pd

def load_security_data(csv_path: str) -> str:
    df = pd.read_csv(csv_path)

    knowledge = ""
    for _, row in df.iterrows():
        knowledge += f"""
Menace: {row.get('menace', '')}
Description: {row.get('description', '')}
Impact: {row.get('impact', '')}
Solution: {row.get('solution', '')}
---
"""
    return knowledge

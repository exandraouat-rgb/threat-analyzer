import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")
print("Clé chargée :", api_key[:10], "...")

client = Anthropic(apiKey=api_key)

response = client.messages.create(
    model="claude-3-sonnet-20240229",
    max_tokens=200,
    messages=[
        {
            "role": "user",
            "content": "Dis bonjour et explique ton rôle en cybersécurité"
        }
    ]
)

print("\nRéponse de Claude :\n")
print(response.content[0].text)

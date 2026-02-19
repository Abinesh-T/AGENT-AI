from get_client import client

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Explain what an AI agent is in one sentence"
)
print(response.text)

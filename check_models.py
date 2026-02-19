from google import genai
import dotenv
import os
dotenv.load_dotenv()

client = genai.Client(api_key=os.getenv("API_KEY"))

models = client.models.list()
for model in models:
    print(model.name)

from google import genai
import dotenv,os

dotenv.load_dotenv()

client = genai.Client(api_key=os.getenv("API_KEY"))

def get_client():
    return client, os.getenv("MODEL_ID", "gemini-2.5-flash")

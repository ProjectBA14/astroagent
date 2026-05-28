from dotenv import load_dotenv
import os

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

PROKERALA_CLIENT_ID = os.getenv(
    "PROKERALA_CLIENT_ID"
)

PROKERALA_CLIENT_SECRET = os.getenv(
    "PROKERALA_CLIENT_SECRET"
)

MODEL_NAME = "llama-3.1-8b-instant"
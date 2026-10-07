from dotenv import load_dotenv
import os

from config.settings import MODEL_NAME
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

model = ChatGoogleGenerativeAI(
  model=MODEL_NAME,
  api_key=GEMINI_API_KEY,
)


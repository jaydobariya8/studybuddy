"""Your first API call to Gemini. Run with:  python hello_gemini.py"""

import os

from dotenv import load_dotenv
from google import genai


load_dotenv()  # reads GEMINI_API_KEY from the .env file next to this script

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents="Hello how are you...",
)

print(response.text)

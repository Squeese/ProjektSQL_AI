import os
from dotenv import load_dotenv
from google import genai

load_dotenv()  # wczytuje klucz z pliku .env
klient = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

odpowiedz = klient.models.generate_content(
    model="gemini-2.5-flash",
    contents="Powiedz po polsku: cześć, działam!"
)
print(odpowiedz.text)
import os
import sqlite3
from dotenv import load_dotenv
from google import genai

load_dotenv()
klient = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

SCIEZKA_BAZY = "data/chinook.db.sqlite"

# Maszynka: uruchamia dowolny SQL i zwraca wyniki
def uruchom_sql(zapytanie):
    polaczenie = sqlite3.connect(SCIEZKA_BAZY)
    kursor = polaczenie.cursor()
    kursor.execute(zapytanie)
    wyniki = kursor.fetchall()
    polaczenie.close()
    return wyniki

# Wyciąga z bazy listę tabel i kolumn, żeby AI wiedziało, co jest dostępne
def pobierz_schemat():
    polaczenie = sqlite3.connect(SCIEZKA_BAZY)
    kursor = polaczenie.cursor()
    kursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tabele = [t[0] for t in kursor.fetchall()]
    opis = []
    for tabela in tabele:
        kursor.execute(f"PRAGMA table_info({tabela})")
        kolumny = [k[1] for k in kursor.fetchall()]
        opis.append(f"{tabela}({', '.join(kolumny)})")
    polaczenie.close()
    return "\n".join(opis)

# Prosi AI, żeby napisało SQL na podstawie pytania po polsku
def napisz_sql(pytanie):
    schemat = pobierz_schemat()
    prompt = f"""Jesteś asystentem piszącym zapytania SQL dla bazy SQLite.
Oto tabele i kolumny w bazie:
{schemat}

Napisz zapytanie SQL odpowiadające na pytanie. Zwróć SAM SQL, bez komentarzy i bez znaczników ```.

Pytanie: {pytanie}"""
    odpowiedz = klient.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return odpowiedz.text.replace("```sql", "").replace("```", "").strip()

# --- Główna część: pytaj w kółko ---
while True:
    pytanie = input("\nZadaj pytanie (lub wpisz 'koniec'): ")
    if pytanie.lower() == "koniec":
        break
    sql = napisz_sql(pytanie)
    print("\nWygenerowany SQL:\n", sql)
    print("\nWynik:")
    for wiersz in uruchom_sql(sql):
        print(wiersz)
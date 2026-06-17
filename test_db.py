import sqlite3

# Maszynka: uruchamia DOWOLNE zapytanie SQL i zwraca wyniki
def uruchom_sql(zapytanie):
    polaczenie = sqlite3.connect("data/chinook.db.sqlite")
    kursor = polaczenie.cursor()
    kursor.execute(zapytanie)
    wyniki = kursor.fetchall()
    polaczenie.close()
    return wyniki

# Test 1: 5 klientów
print("Klienci:")
for wiersz in uruchom_sql("SELECT FirstName, LastName, Country FROM Customer LIMIT 5"):
    print(wiersz)

# Test 2: kraje wg wydatków (z JOIN-em)
print("\nKraje wg wydatkow:")
zapytanie2 = """
SELECT c.Country, SUM(i.Total) AS wydatki
FROM Customer c
JOIN Invoice i ON c.CustomerId = i.CustomerId
GROUP BY c.Country
ORDER BY wydatki DESC
LIMIT 5
"""
for wiersz in uruchom_sql(zapytanie2):
    print(wiersz)
import requests
import pandas as pd
from datetime import datetime
import os

# Remplace par tes identifiants Myfxbook !
email = "mallein38590@gmail.com"
password = "pibdUr-tasdo7-bazvav"

# Étape 1 : Login pour obtenir session ID
login_url = f"https://www.myfxbook.com/api/login.json?email={email}&password={password}"
r = requests.get(login_url)
print(r.text)  # Montre la réponse brute, même si ce n'est pas du JSON
try:
    login_data = r.json()
    print(login_data)
except Exception as e:
    print("Erreur de décodage JSON :", e)
    exit()

session_id = login_data["session"]

# Étape 2 : Requête sentiment
sentiment_url = f"https://www.myfxbook.com/api/get-community-outlook.json?session={session_id}"
r = requests.get(sentiment_url)
print(r.text)  # Ajoute ça pour voir la réponse
try:
    data = r.json()
    print(data)
except Exception as e:
    print("Erreur de décodage JSON :", e)
    exit()

# Recherche des paires de devises dans le dictionnaire (clé 'name')
rows = []
for v in data.values():
    if isinstance(v, list):
        rows = v
        break

if not rows:
    print("Aucune donnée de sentiment détaillée trouvée !")
    exit()

result = []
for row in rows:
    if "name" in row:  # Cible les entrées qui sont bien des paires
        pair = row["name"]
        long_perc = float(row.get("longPercentage", 0))
        short_perc = float(row.get("shortPercentage", 0))
        result.append([
            pair,
            long_perc,
            short_perc,
            datetime.now().strftime('%Y-%m-%d %H:%M')
        ])

df = pd.DataFrame(result, columns=["Pair", "Long (%)", "Short (%)", "Updated"])
os.makedirs("data", exist_ok=True)
df.to_csv("data/sentiment.csv", index=False)
print("Sentiment retail Myfxbook sauvegardé dans data/sentiment.csv")

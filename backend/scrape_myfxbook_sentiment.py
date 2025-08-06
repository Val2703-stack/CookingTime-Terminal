import requests
import pandas as pd
from datetime import datetime
import os
import time

# Remplace par tes identifiants Myfxbook !
email = "mallein38590@gmail.com"
password = "27Mars2003@@"

MAX_ATTEMPTS = 2
WAIT_TIME = 30  # secondes à attendre entre deux tentatives si bloqué

def login_myfxbook(email, password):
    login_url = f"https://www.myfxbook.com/api/login.json?email={email}&password={password}"
    for attempt in range(1, MAX_ATTEMPTS + 1):
        print(f"Tentative de login {attempt}...")
        r = requests.get(login_url)
        print(r.text)
        try:
            login_data = r.json()
            print(login_data)
        except Exception as e:
            print("Erreur de décodage JSON :", e)
            return None

        # Gestion des erreurs spécifiques
        if "error" in login_data and login_data["error"]:
            msg = login_data.get("message", "")
            if "Max login attempts reached" in msg:
                print("Trop de tentatives, on attend pour éviter d'être banni...")
                time.sleep(WAIT_TIME)
                continue
            else:
                print("Erreur lors du login :", msg)
                return None
        session_id = login_data.get("session", "")
        if session_id:
            return session_id
        else:
            print("Pas de session_id reçu.")
            time.sleep(WAIT_TIME)
    return None

session_id = login_myfxbook(email, password)
if not session_id:
    print("Impossible d'obtenir une session Myfxbook, arrêt du script.")
    exit()

# Étape 2 : Requête sentiment
sentiment_url = f"https://www.myfxbook.com/api/get-community-outlook.json?session={session_id}"
r = requests.get(sentiment_url)
print(r.text)
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
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
csv_save_path = os.path.join(CURRENT_DIR, "..", "frontend", "data", "sentiment.csv")
os.makedirs(os.path.dirname(csv_save_path), exist_ok=True)
df.to_csv(csv_save_path, index=False)
print(f"Sentiment retail Myfxbook sauvegardé dans {csv_save_path}")



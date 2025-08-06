import pandas as pd
import zipfile
import requests
from io import BytesIO
import os
from datetime import datetime

# Dossier et chemin du CSV exporté
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
local_csv = os.path.join(CURRENT_DIR, "..", "frontend", "data", "cot_financial_full.csv")

def download_and_save_full_cot_financial(local_csv):
    year = datetime.now().year
    url = f"https://www.cftc.gov/files/dea/history/fut_fin_txt_{year}.zip"

    print(f"Téléchargement du COT Financial Futures {year} ...")
    r = requests.get(url)
    if r.status_code != 200:
        print(f"Erreur lors du téléchargement de {url}")
        return

    z = zipfile.ZipFile(BytesIO(r.content))
    file_name = z.namelist()[0]
    df = pd.read_csv(z.open(file_name), sep=",", engine="python", skiprows=0)

    # Ajoute la position nette pour chaque catégorie principale
    df['Net_Dealer']        = df['Dealer_Positions_Long_All']        - df['Dealer_Positions_Short_All']
    df['Net_AssetManager']  = df['Asset_Mgr_Positions_Long_All']     - df['Asset_Mgr_Positions_Short_All']
    df['Net_LevFunds']      = df['Lev_Money_Positions_Long_All']     - df['Lev_Money_Positions_Short_All']
    df['Net_OtherReport']   = df['Other_Rept_Positions_Long_All']    - df['Other_Rept_Positions_Short_All']
    df['Net_NonReport']     = df['NonRept_Positions_Long_All']       - df['NonRept_Positions_Short_All']

    # Liste des colonnes à exporter (toutes les catégories, net positions, code, marché, date)
    columns = [
        'As_of_Date_In_Form_YYMMDD', 'Market_and_Exchange_Names', 'CFTC_Contract_Market_Code',
        # Dealer/Intermediary
        'Dealer_Positions_Long_All', 'Dealer_Positions_Short_All', 'Dealer_Positions_Spread_All', 'Net_Dealer',
        # Asset Manager/Institutional
        'Asset_Mgr_Positions_Long_All', 'Asset_Mgr_Positions_Short_All', 'Asset_Mgr_Positions_Spread_All', 'Net_AssetManager',
        # Leverage Funds
        'Lev_Money_Positions_Long_All', 'Lev_Money_Positions_Short_All', 'Lev_Money_Positions_Spread_All', 'Net_LevFunds',
        # Other Reportables
        'Other_Rept_Positions_Long_All', 'Other_Rept_Positions_Short_All', 'Other_Rept_Positions_Spread_All', 'Net_OtherReport',
        # Nonreportable
        'NonRept_Positions_Long_All', 'NonRept_Positions_Short_All', 'Net_NonReport'
    ]
    columns = [col for col in columns if col in df.columns]  # sécurité si des colonnes manquent

    result = df[columns]

    os.makedirs(os.path.dirname(local_csv), exist_ok=True)
    result.to_csv(local_csv, index=False)
    print(f"\n✅ Fichier Financial Futures complet exporté ici :\n{local_csv}")

if __name__ == "__main__":
    download_and_save_full_cot_financial(local_csv)

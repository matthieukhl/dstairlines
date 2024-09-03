import pandas as pd
from sqlalchemy import create_engine
from db_connection import create_connection

# Initialiser le dataframe
countries = pd.read_csv("/Users/matthieukhl/Documents/trainingbs4/data/world-data-2023.csv")

# Renommage des colonnes
rename_dict = {
    "Country": "country",
    "Abbreviation": "code",
    "Capital/Major City": "capital",
    "Latitude": "latitude",
    "Longitude": "longitude"
}
countries.rename(columns=rename_dict, inplace=True)

# Création d'un nouveau DataFrame avec les noms de colonnes modifiés
countries = countries[['country', 'code', 'capital', 'latitude', 'longitude']]

# Créer l'URL de connexion pour SQLAlchemy
engine = create_connection()

# Écrire le DataFrame dans la table PostgreSQL
table_name = 'countries'
countries.to_sql(table_name, engine, index=False, if_exists='append')  # 'append' pour ajouter des données à une table existante

print("Data has been uploaded successfully.")
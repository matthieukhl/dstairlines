import pandas as pd
import numpy as np
import os
from sqlalchemy import create_engine
from db_connection import create_connection
from bs4 import BeautifulSoup
import requests

# Initialisation de variables
engine = create_connection() # Création de la connexion à la base
current_dir = os.path.dirname(__file__) 

# Import countries data in countries table
countries_path = os.path.join(current_dir, "..", "..", "data", "raw", "world-data-2023.csv")
countries_df = pd.read_csv(countries_path)

# Renommage des colonnes
countries_dict = {
    "Country": "country",
    "Abbreviation": "code",
    "Capital/Major City": "capital",
    "Latitude": "latitude",
    "Longitude": "longitude"
}
countries_df.rename(columns=countries_dict, inplace=True)

# Création d'un nouveau DataFrame avec les noms de colonnes modifiés
countries_df = countries_df[['country', 'code', 'capital', 'latitude', 'longitude']]

# Écrire les DataFrames dans la base MySQL
table_countries = 'countries_df'
countries_df.to_sql(table_countries, engine, index=False, if_exists='append') 

print("Countries data has been uploaded successfully.")

# Import airports data from Wikipedia
base_url = "https://en.wikipedia.org/wiki/List_of_airports_by_IATA_airport_code:_"

# Création d'un DF vide pour stocker les données
airports_columns = ['iata', 'icao', 'name', 'city', 'country', 'timezone']
airports_df = pd.DataFrame(columns=airports_columns)

# Liste temporaire pour stocker les nouvelles lignes
rows_list = []

# Boucle sur les lettres de l'alphabet
for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
    # Construction de l'URL
    url = f"{base_url}{letter}"
    
    # Requête HTTP
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Trouver la table contenant les données des aéroports
    tables = soup.find_all("table", {"class": "wikitable sortable"})
    
    if tables:
        # Analyser la première table trouvée (la principale)
        for row in tables[0].find_all('tr')[1:]:
            cols = row.find_all("td")
            if len(cols) > 4:  # Assurer que la rangée contient toutes les données nécessaires
                iata = cols[0].text.strip()
                icao = cols[1].text.strip()
                airport_name = cols[2].text.strip()
                location = cols[3].text.strip()
                timezone = cols[4].text.strip()
                
                # Séparer city et country en ignorant une éventuelle région
                location_parts = location.split(',')
                
                if len(location_parts) == 2:  # Si seulement ville et pays sont présents
                    city = location_parts[0].strip()
                    country = location_parts[1].strip()
                elif len(location_parts) > 2:  # Si une région est présente, l'ignorer
                    city = location_parts[0].strip()
                    country = location_parts[-1].strip()
                else:
                    city = location
                    country = ""

                # Ajout des données dans la liste temporaire
                rows_list.append({'iata': iata, 'icao': icao, 'name': airport_name, 'city': city, 'country': country, 'timezone': timezone})

# Conversion de la liste en DataFrame
airports_df = pd.DataFrame(rows_list, columns=airports_columns)

# Écrire le DataFrame dans la table PostgreSQL
airports_table = 'airports'
airports_df.to_sql(airports_table, engine, index=False, if_exists='append')  # 'append' pour ajouter des données à une table existante

print("Airports data has been uploaded successfully.")
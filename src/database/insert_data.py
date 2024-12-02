import pandas as pd
import numpy as np
import os
from db_connection import create_connection
from sqlalchemy import create_engine
from bs4 import BeautifulSoup
import requests

# Initialisation de variables
engine = create_connection() # Création de la connexion à la base
current_dir = os.path.dirname(__file__) 

# Import countries function
def import_countries(engine):
    countries_path = os.path.join(current_dir, "..", "..", "data", "raw", "world-data-2023.csv")
    countries_df = pd.read_csv(countries_path)

    # Rename columns
    countries_dict = {
        "Country": "country",
        "Abbreviation": "code",
        "Capital/Major City": "capital",
        "Latitude": "latitude",
        "Longitude": "longitude"
    }
    
    countries_df.rename(columns=countries_dict, inplace=True)

    # Create new Dataframe with renamed columns
    countries_df = countries_df[['country', 'code', 'capital', 'latitude', 'longitude']]

    # Écrire les DataFrames dans la base MySQL
    countries_table  = "countries"
    countries_df.to_sql(countries_table, engine, index=False, if_exists='append') 

    print("Countries data has been uploaded successfully.")

# Import airports data from Wikipedia function
def import_airports(engine):    
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

# Import aircrafts data from Wikipedia Function
def import_aircrafts(engine):
    aircrafts_url = "https://en.wikipedia.org/wiki/List_of_commercial_jet_airliners"
    response = requests.get(aircrafts_url)
    print(response.status_code)

    # Parse HTML data into a BeautifulSoup object
    soup = BeautifulSoup(response.text, "html.parser")
    tables = soup.find_all("table", {'class': "wikitable"})

    # Convert HTML tables to DataFrame objects
    df_list = pd.read_html(str(tables))
    df_current, df_planned, df_oop, df_historical = df_list[0], df_list[1], df_list[2], df_list[3]
    print(df_historical.columns)

    # Rename columns to maintain consistency and readability
    rename_dict = {
        "Type": "model_name",
        "Country": "country",
        "Origin": "country",
        "Engines[a]": "engines",
        "Engines[c]": "engines",
        "Engines[e]": "engines",
        "Engines[h]": "engines",
        "First flight": "first_flight",
        "Airline service entry": "airline_service_entry",
        "End of production": "end_of_production",
        "Number built": "number_built",
        "In service[1][b]": "nb_in_service",
        "In service [1][d]": "nb_in_service",
        "In service[1][f]": "nb_in_service",
        "Year retired[i]": "year_retired"
    }

    # Apply renaming across all dataframes
    df_current.rename(columns=rename_dict, inplace=True)
    df_planned.rename(columns=rename_dict, inplace=True)
    df_oop.rename(columns=rename_dict, inplace=True)
    df_historical.rename(columns=rename_dict, inplace=True)

    # Cleaning data for df_current
    # Splits the string at the first space and retains only first part of entry
    df_current['number_built'] = df_current['number_built'].str.split().str[0]
    df_current['nb_in_service'] = df_current['nb_in_service'].str.split().str[0]

    # Deletes commas
    df_current['number_built'] = df_current['number_built'].str.replace(',', '')
    df_current['nb_in_service'] = df_current['nb_in_service'].str.replace(',', '')

    # Converts the column in int64 and deals errors with NaN
    df_current['number_built'] = pd.to_numeric(df_current['number_built'], errors='coerce')
    df_current['nb_in_service'] = pd.to_numeric(df_current['nb_in_service'], errors='coerce')

    # Cleaning data for df_oop 
    #country column
    df_oop["country"] = df_oop["country"].str.replace(r"\s*\[[^\]]*\]", "", regex=True)

    # Clean and convert number_built column to int64
    df_oop['number_built'] = df_oop['number_built'].str.replace(r"\s*\[[^\]]*\]", "", regex=True)
    df_oop['nb_in_service'] = df_oop['nb_in_service'].str.split().str[0]

    # Clean and convert nb_in_service column to int64
    df_oop['nb_in_service'] = df_oop['nb_in_service'].str.replace(',', '')
    df_oop['number_built'] = df_oop['number_built'].str.replace(',', '')
    df_oop['nb_in_service'] = pd.to_numeric(df_oop['nb_in_service'], errors='coerce')
    df_oop['number_built'] = pd.to_numeric(df_oop['number_built'], errors='coerce')

    # df_historical Data Cleaning
    # country column
    df_historical["country"] = df_historical["country"].str.replace(r"\s*\[[^\]]*\]", "", regex=True)

    # engines column
    df_historical['engines'] = df_historical['engines'].str.replace(r"\s*\[[^\]]*\]", "", regex=True)
    df_historical['engines'] = pd.to_numeric(df_historical['engines'], errors='coerce')

    # airline_service_entry column
    df_historical['airline_service_entry'] = pd.to_numeric(df_historical['airline_service_entry'], errors='coerce')
    df_historical['airline_service_entry'] = df_historical['airline_service_entry'].astype('Int64')

    # year_retired column
    df_historical['year_retired'] = df_historical["year_retired"].str.split().str[0]
    df_historical['year_retired'] = pd.to_numeric(df_historical['year_retired'], errors='coerce')
    df_historical['year_retired'] = df_historical['year_retired'].astype('Int64')

    # Cleaning data for df_planned
    #first_flight column
    df_planned['first_flight'] = pd.to_numeric(df_planned['first_flight'], errors='coerce')
    df_planned['first_flight'] = df_planned['first_flight'].astype("Int64")

    # airline_service_entry column
    df_planned['airline_service_entry'] = df_planned['airline_service_entry'].str.split().str[0]
    df_planned['airline_service_entry'] = pd.to_numeric(df_planned['airline_service_entry'], errors='coerce')
    df_planned['airline_service_entry'] = df_planned['airline_service_entry'].astype('Int64')

    # end_of_production
    df_planned['end_of_production'] = pd.to_numeric(df_planned['end_of_production'], errors='coerce')

    # number_built
    df_planned['number_built'] = df_planned['number_built'].astype('Int64')

    # nb_in_service
    df_planned['nb_in_service'] = df_planned["nb_in_service"].astype('Int64')

    # Concaténer les quatre DataFrames
    df_concatenated = pd.concat(
        [df_current, df_planned, df_oop, df_historical],
        axis=0,           # Concaténation verticale
        ignore_index=True, # Réinitialise les indices
        sort=False         # Évite de trier les colonnes
    )

    # Écrire le DataFrame dans la table PostgreSQL
    table_name = 'aircrafts'
    df_concatenated.to_sql(table_name, engine, index=False, if_exists='append')  # 'append' pour ajouter des données à une table existante

    print("Aircraft data has been uploaded successfully.")
    
# Main Function
def main():
    import_countries(engine)
    import_airports(engine)
    import_aircrafts(engine)
    
if __name__ == "__main__":
    main()
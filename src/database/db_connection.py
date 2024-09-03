import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

#Charge les variables d'environnement depuis le fichier .env
load_dotenv()

# Récupérer les informations de connexion depuis les variables d'environnement
DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

# Construire l'URL de connexion à la base de données
DATABASE_URL = f"mysql+mysqlconnector://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Fonction pour créer et retourner un moteur SQLAlchemy
def create_connection():
    """
    create_engine utilise l'URL de connexion construire pour créer un objet engine. 
    Cet objet est reponsable de la gestion de la connexion à la base de données.
    Il est utilisé pour exécuter des requêtes SQL, établir des sessions, et bien plus encore.
    """
    engine = create_engine(DATABASE_URL)
    return engine
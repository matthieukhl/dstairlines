import os
from sqlalchemy import create_engine, Column, Integer, String, DECIMAL, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Récupérer les informations de connexion depuis les variables d'environnement
DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

# Construire l'URL de connexion à la base de données
DATABASE_URL = f"mysql+mysqlconnector://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Créer le moteur SQLAlchemy
engine = create_engine(DATABASE_URL)

# Déclarer la base pour les modèles
Base = declarative_base()

# Définir les modèles pour les tables
class Airport(Base):
    __tablename__ = 'airports'
    id = Column(Integer, primary_key=True, autoincrement=True)
    iata_code = Column(String(3), unique=True, nullable=False)
    name = Column(String(100))
    city = Column(String(100))
    country = Column(String(100))
    latitude = Column(DECIMAL(9, 6))
    longitude = Column(DECIMAL(9, 6))

class Aircraft(Base):
    __tablename__ = 'aircrafts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    registration = Column(String(20), nullable=False)
    model = Column(String(50))
    airline = Column(String(50))
    icao_code = Column(String(4))

class Flight(Base):
    __tablename__ = 'flights'
    id = Column(Integer, primary_key=True, autoincrement=True)
    flight_number = Column(String(10), nullable=False)
    departure_airport = Column(String(3), ForeignKey('airports.iata_code'))
    arrival_airport = Column(String(3), ForeignKey('airports.iata_code'))
    scheduled_departure = Column(DateTime)
    scheduled_arrival = Column(DateTime)
    status = Column(String(50))
    aircraft_id = Column(Integer, ForeignKey('aircrafts.id'))

# Créer toutes les tables
def create_tables():
    Base.metadata.create_all(engine)
    print("Tables created successfully")

if __name__ == "__main__":
    create_tables()
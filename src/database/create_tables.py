from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from db_connection import create_connection

# Création de la connexion avec create_connection
engine = create_connection()

# Requêtes SQL pour créer les tables
CREATE_TABLE_QUERIES = [
    """CREATE TABLE airports (
    id INT AUTO_INCREMENT PRIMARY KEY,
    iata_code VARCHAR(3) UNIQUE,
    name VARCHAR(100),
    city VARCHAR(100),
    country VARCHAR(100),
    latitude DECIMAL(9,6),
    longitude DECIMAL(9,6)
);
    """,
    """CREATE TABLE aircrafts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    registration VARCHAR(20) NOT NULL,
    model VARCHAR(50),
    airline VARCHAR(50),
    icao_code VARCHAR(4)
);
    """,
    """CREATE TABLE flights (
    id INT AUTO_INCREMENT PRIMARY KEY,
    flight_number VARCHAR(10) NOT NULL,
    departure_airport VARCHAR(3),
    arrival_airport VARCHAR(3),
    scheduled_departure DATETIME,
    scheduled_arrival DATETIME,
    status VARCHAR(50),
    aircraft_id INT,
    FOREIGN KEY (departure_airport) REFERENCES airports(iata_code),
    FOREIGN KEY (arrival_airport) REFERENCES airports(iata_code),
    FOREIGN KEY (aircraft_id) REFERENCES aircrafts(id)
);
    """,
    """CREATE TABLE countries (
	id INT AUTO_INCREMENT PRIMARY KEY,
    country VARCHAR(100) NOT NULL,
    code VARCHAR(2) DEFAULT NULL,
    capital VARCHAR(100) DEFAULT NULL,
    latitude VARCHAR(36) DEFAULT NULL,
    longitude VARCHAR(36) DEFAULT NULL
);
    """
]
# Créer toutes les tables
def create_tables():
    with engine.connect() as connection:
        for query in CREATE_TABLE_QUERIES:
            try:
                connection.execute(text(query))
                print("Table created successfully")
            except SQLAlchemyError as e:
                print(f"Error occured: {e}")

if __name__ == "__main__":
    create_tables()
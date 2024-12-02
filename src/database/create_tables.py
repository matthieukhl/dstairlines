from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from db_connection import create_connection

# Création de la connexion avec create_connection
engine = create_connection()

# Requêtes SQL pour créer les tables
CREATE_TABLE_QUERIES = [
    """CREATE TABLE airports (
    id INT AUTO_INCREMENT PRIMARY KEY,
    iata VARCHAR(10) UNIQUE,
    icao VARCHAR(10) DEFAULT NULL,
    name VARCHAR(100),
    city VARCHAR(100),
    country VARCHAR(100),
    timezone VARCHAR(50)
);
    """,
    """CREATE TABLE aircrafts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    model_name VARCHAR(50) NOT NULL,
    country VARCHAR(100) DEFAULT NULL,
    engines INT DEFAULT NULL,
    first_flight YEAR DEFAULT NULL,
    airline_service_entry YEAR DEFAULT NULL,
    number_built INT DEFAULT NULL,
    nb_in_service INT DEFAULT NULL,
    end_of_production YEAR DEFAULT NULL,
    year_retired YEAR DEFAULT NULL
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
    FOREIGN KEY (departure_airport) REFERENCES airports(iata),
    FOREIGN KEY (arrival_airport) REFERENCES airports(iata),
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
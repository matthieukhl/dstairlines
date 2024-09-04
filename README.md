# Flight Tracker Project

## Setup de l'environnement

### Prérequis

- Python 3.x
- pip
- Git
- Docker (pour lancer MySQL dans un conteneur)

### 1. Cloner le dépôt

```bash
git clone https://github.com/ton-utilisateur/ton-repo.git
cd ton-repo
```

### 2. Créer un environnement virtuel
```bash
python3 -m venv venv
source venv/bin/activate  # Sous macOS/Linux
venv\Scripts\activate  # Sous Windows
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```
### 4. Configurer les variables d'environnement
Créez un fichier `.env` à la racine du projet avec les variables nécessaires.
```bash
DB_USERNAME=nom_d_utilisateur
DB_PASSWORD=mot_de_passe
DB_HOST=adresse_du_server
DB_PORT=3306
DB_NAME=flight_tracker
```

Pour streamlit créez à la racine du projet le fichier `/.streamlit/secrets.toml`
```bash
mkdir .streamlit
touch .streamlit/secrets.toml
```

Complétez la configuration suivante avec les informations d'accès à votre base de données MySQL :
```toml
[connections.mysql]
dialect = "mysql"
host = "127.0.0.1"
port = 3306
database = "flight_tracker"
username = "username"
password = "password"
query = { charset = "utf8mb4" }
````

### 5. Lancer MySQL avec Docker

1. Vérifiez l'installation de Docker
Pour lancer une instance MySQL en utilisant Docker, vérifiez que Docker est bien installé :
```bash
docker --version
```

Si Docker n'est pas installé, vous pouvez le télécharger et l'installer depuis le site officiel de Docker.

2. Lancez une instance MySQL avec Docker
```bash
docker run --name mysql-container -e MYSQL_ROOT_PASSWORD=yourpassword -e MYSQL_DATABASE=flight_tracker -p 3306:3306 -d mysql:latest
```

3. Accédez à MySQL
```bash
docker exec -it mysql-container mysql -u root -p
```

4. Créez la base flight_tracker
```sql
CREATE DATABASE flight_tracker
```

5. Arrêt et suppression du conteneur MySQL
```bash
docker stop mysql-container
docker rm mysql-container
```

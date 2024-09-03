# Flight Tracker Project

## Setup de l'environnement

### Prérequis

- Python 3.x
- pip
- Git

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

### 3. Instaler les dépendances
```bash
pip install -r requirements.txt
```
### 4. Configurer les variables d'environnement
Créez un fichier `.env` à la racine du projet avec les variables nécessaires.
```bash
DB_USERNAME=ton_nom_d_utilisateur
DB_PASSWORD=ton_mot_de_passe
DB_HOST=l'adresse_de_ton_serveur
DB_PORT=3306
DB_NAME=flight_tracker
```

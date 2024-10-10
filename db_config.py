from sqlalchemy import create_engine
from urllib.parse import quote

def connect_to_db(config):
    db_url = f"mysql+mysqlconnector://{config['user']}:{quote(config['password'])}@{config['host']}:{config.get('port', '3306')}/{config['database']}"
    try:
        engine = create_engine(db_url)
        conn = engine.connect()
        print(f"Connexion à la base de données {config['database']} réussie")
        return conn
    except Exception as err:
        print(f"Erreur lors de la connexion à la base de données: {err}")
        return None

configurations = {
    'PROD': {
        'parking_db': {
            'user': 'ericrj',
            'password': '1610',
            'host': 'localhost',
            'port': '3306',
            'database': 'parking_db'
        }
    }
}

def get_connection(environment, db_name):
    config = configurations[environment][db_name]
    return connect_to_db(config)

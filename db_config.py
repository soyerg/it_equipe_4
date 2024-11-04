from sqlalchemy import create_engine
from urllib.parse import quote

def get_db_url(config):
    return f"mysql+mysqlconnector://{config['user']}:{quote(config['password'])}@{config['host']}:{config.get('port', '3306')}/{config['database']}?charset=utf8mb4&collation=utf8mb4_general_ci"

configurations = {
    # 'DEV': {
    #     'parking_db': {
    #         'user': 'root',
    #         'password': 'rootroot',
    #         'host': 'it-chaircapgemini.c1q8gu2s6pm0.eu-north-1.rds.amazonaws.com',

    #         'port': '3306',
    #         'database': 'parking_db'
    #     }
    # },
    'PROD': {
        'parking_db': {
            'user': 'ericrj',
            'password': '1610',
            'host': 'host.docker.internal',
            'port': '3306',
            'database': 'parking_db'
        }
    }
}

def get_connection(environment, db_name):
    config = configurations[environment][db_name]
    return get_db_url(config)

import subprocess
from werkzeug.security import generate_password_hash
from faker import Faker
import random
from datetime import datetime, timedelta
from db_config import get_connection

db_url = get_connection('PROD', 'parking_db')

config = {
    'user': db_url.split('//')[1].split(':')[0],
    'password': db_url.split(':')[2].split('@')[0],
    'host': db_url.split('@')[1].split(':')[0],
    'port': db_url.split(':')[-1].split('/')[0],
}

mysql_executable_path = "mysql"
fake = Faker('fr_FR')

# Utilisateurs prédéfinis
users_data = [
    "reda.belghiti@test.fr", "zakary.belkacem@test.fr", "anatole.boittiaux@test.fr",
    "jules.buvry@test.fr", "anthinea.camman@test.fr", "thomas.ferrato@test.fr",
    "ange-dylan.gnaglo@test.fr", "celia.heng@test.fr", "camille.heng@test.fr",
    "paul.im-saroeun@test.fr", "neo.jonas@test.fr", "ryan.khou@test.fr",
    "remi.labou@test.fr", "alexandre.macchi@test.fr", "benjamin.msika@test.fr",
    "ndongomedoune.ndiaye@test.fr", "nihad.nhar@test.fr", "ferdinand.perez@test.fr",
    "cyril.petris@test.fr", "enzo.pin@test.fr", "cyprien.pivert@test.fr",
    "corentin.poupry@test.fr", "eric.rajiban@edu.esiee.fr", "alexis.simon@test.fr",
    "gabriel.soyer@test.fr", "gregoire.ugolini@test.fr", "brieuc.valence@test.fr"
]

special_users = [
    {"username": "user", "email": "user@test.fr", "role_id": 3, "password": "1234"},
    {"username": "admin", "email": "admin@test.fr", "role_id": 1, "password": "1234"},
    {"username": "agent", "email": "agent@test.fr", "role_id": 2, "password": "1234"},
]

def execute_sql(database_name, sql_query):
    command = [
        mysql_executable_path,
        '-u', config['user'],
        '-p' + config['password'],
        '-h', config['host'],
        '-P', config['port'],
        database_name,
        '-e', sql_query
    ]
    subprocess.run(command, check=True)

def fetch_sql(database_name, sql_query):
    command = [
        mysql_executable_path,
        '-u', config['user'],
        '-p' + config['password'],
        '-h', config['host'],
        '-P', config['port'],
        database_name,
        '-e', sql_query
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout.strip()

def clear_existing_data():
    tables = ['Payment', 'ParkingReservation', 'ParkingSpot', 'Vehicle', 'User', 'VehicleType']
    for table in tables:
        sql_delete = f"DELETE FROM {table};"
        execute_sql('parking_db', sql_delete)
    print("Les données existantes ont été supprimées.")

def generate_random_password():
    return fake.password(length=10)

def format_username(email):
    name_parts = email.split('@')[0].split('.')
    return ''.join(part.capitalize() for part in name_parts)

def insert_test_data():
    # Insertion des utilisateurs prédéfinis avec des rôles au hasard
    for email in users_data:
        username = format_username(email)
        password_hash = generate_password_hash(generate_random_password())
        role_id = random.choice([2, 3])  # Role 2 (agent) ou Role 3 (usager)
        sql_insert_user = f"""
        INSERT INTO User (username, email, password_hash, role_id, active)
        VALUES ('{username}', '{email}', '{password_hash}', {role_id}, TRUE);
        """
        execute_sql('parking_db', sql_insert_user)

    # Insertion des utilisateurs spéciaux
    for user in special_users:
        password_hash = generate_password_hash(user["password"])
        sql_insert_special_user = f"""
        INSERT INTO User (username, email, password_hash, role_id, active)
        VALUES ('{user["username"]}', '{user["email"]}', '{password_hash}', {user["role_id"]}, TRUE);
        """
        execute_sql('parking_db', sql_insert_special_user)

    # Récupérer les IDs des utilisateurs après insertion
    user_ids_query = "SELECT id FROM User;"
    user_ids = fetch_sql('parking_db', user_ids_query).split('\n')[1:]

    # Insertion des types de véhicules
    vehicle_types = ['Voiture', 'Moto', 'Camion', 'Scooter', 'Vélo électrique']
    for vehicle_type in vehicle_types:
        sql_insert_vehicle_type = f"INSERT INTO VehicleType (type_name) VALUES ('{vehicle_type}');"
        execute_sql('parking_db', sql_insert_vehicle_type)

    # Récupérer les IDs des types de véhicules
    vehicle_type_ids_query = "SELECT id FROM VehicleType;"
    vehicle_type_ids = fetch_sql('parking_db', vehicle_type_ids_query).split('\n')[1:]

    # Insertion des véhicules
    for _ in range(20):
        license_plate = fake.license_plate()
        owner_id = random.choice(user_ids)
        vehicle_type_id = random.choice(vehicle_type_ids)
        sql_insert_vehicle = f"""
        INSERT INTO Vehicle (license_plate, owner_id, vehicle_type_id)
        VALUES ('{license_plate}', {owner_id}, {vehicle_type_id});
        """
        execute_sql('parking_db', sql_insert_vehicle)

    # Récupérer les IDs des véhicules après insertion
    vehicle_ids_query = "SELECT id FROM Vehicle;"
    vehicle_ids = fetch_sql('parking_db', vehicle_ids_query).split('\n')[1:]

    # Insertion des places de parking
    for i in range(20):
        spot_number = f"SP-{i+1}"
        status = random.choice(['libre', 'occupée'])
        # Associe un véhicule uniquement si le spot est occupé
        vehicle_id = random.choice(vehicle_ids) if status == 'occupée' else 'NULL'
        spot_type = random.choice(['normale', 'handicapé', '2 roues', 'électrique'])
        sql_insert_parking_spot = f"""
        INSERT INTO ParkingSpot (spot_number, status, vehicle_id, spot_type)
        VALUES ('{spot_number}', '{status}', {vehicle_id}, '{spot_type}');
        """
        execute_sql('parking_db', sql_insert_parking_spot)

    # Récupérer les IDs des places de parking après insertion
    parking_spot_ids_query = "SELECT id FROM ParkingSpot;"
    parking_spot_ids = fetch_sql('parking_db', parking_spot_ids_query).split('\n')[1:]

    # Insertion des réservations de parking
    for _ in range(20):
        user_id = random.choice(user_ids)
        parking_spot_id = random.choice(parking_spot_ids)  # Utilise les IDs de places de parking existants
        start_time = fake.date_time_between(start_date='-2d', end_date='now')
        end_time = start_time + timedelta(minutes=random.randint(30, 120))  # Durée de réservation entre 30 mins et 2 heures
        amount_paid = round(random.uniform(5, 15), 2)
        payment_status = random.choice(['payé', 'échoué'])
        sql_insert_reservation = f"""
        INSERT INTO ParkingReservation (user_id, parking_spot_id, start_time, end_time, amount_paid, payment_status)
        VALUES ({user_id}, {parking_spot_id}, '{start_time}', '{end_time}', {amount_paid}, '{payment_status}');
        """
        execute_sql('parking_db', sql_insert_reservation)

    # Récupérer les IDs des réservations après insertion
    reservation_ids_query = "SELECT id FROM ParkingReservation;"
    reservation_ids = fetch_sql('parking_db', reservation_ids_query).split('\n')[1:]

    # Insertion des paiements
    for _ in range(20):
        reservation_id = random.choice(reservation_ids)
        payment_method = random.choice(['carte bancaire', 'PayPal'])
        payment_date = fake.date_time_between(start_date='-1d', end_date='now')
        amount = round(random.uniform(5, 15), 2)
        sql_insert_payment = f"""
        INSERT INTO Payment (reservation_id, payment_method, payment_date, amount)
        VALUES ({reservation_id}, '{payment_method}', '{payment_date}', {amount});
        """
        execute_sql('parking_db', sql_insert_payment)

    print("Les données de test ont été insérées avec succès.")

if __name__ == "__main__":
    clear_existing_data()
    insert_test_data()

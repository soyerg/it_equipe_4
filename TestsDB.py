import subprocess
from werkzeug.security import generate_password_hash
from faker import Faker
import random

config = {
    'user': 'ericrj',
    'password': '1610',
    'host': 'localhost',
    'port': '3306'
}

mysql_executable_path = r"C:\Program Files\MariaDB 11.4\bin\mysql.exe"
fake = Faker('fr_FR')

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

def insert_test_data():
    for _ in range(20):
        username = fake.user_name()
        email = fake.email()
        password_hash = generate_password_hash('password123')
        role_id = random.choice([2, 3])
        sql_insert_user = f"""
        INSERT INTO User (username, email, password_hash, role_id, active)
        VALUES ('{username}', '{email}', '{password_hash}', {role_id}, TRUE);
        """
        execute_sql('parking_db', sql_insert_user)

    user_ids_query = "SELECT id FROM User;"
    user_ids = fetch_sql('parking_db', user_ids_query).split('\n')[1:]

    vehicle_types = ['Voiture', 'Moto', 'Camion', 'Scooter', 'Vélo électrique']
    for vehicle_type in vehicle_types:
        sql_insert_vehicle_type = f"INSERT INTO VehicleType (type_name) VALUES ('{vehicle_type}');"
        execute_sql('parking_db', sql_insert_vehicle_type)

    for _ in range(20):
        license_plate = fake.license_plate()
        owner_id = random.choice(user_ids)  # Utilise un user_id valide
        vehicle_type_id = random.randint(1, len(vehicle_types))
        sql_insert_vehicle = f"""
        INSERT INTO Vehicle (license_plate, owner_id, vehicle_type_id)
        VALUES ('{license_plate}', {owner_id}, {vehicle_type_id});
        """
        execute_sql('parking_db', sql_insert_vehicle)

    for i in range(20):
        spot_number = f"SP-{i+1}"
        status = random.choice(['libre', 'occupée'])
        vehicle_id = 'NULL' if status == 'libre' else random.randint(1, 20)
        spot_type = random.choice(['normale', 'handicapé', '2 roues', 'électrique'])
        sql_insert_parking_spot = f"""
        INSERT INTO ParkingSpot (spot_number, status, vehicle_id, spot_type)
        VALUES ('{spot_number}', '{status}', {vehicle_id}, '{spot_type}');
        """
        execute_sql('parking_db', sql_insert_parking_spot)

    for _ in range(20):
        user_id = random.choice(user_ids)
        parking_spot_id = random.randint(1, 20)
        start_time = fake.date_time_this_year()
        end_time = fake.date_time_this_year()
        amount_paid = round(random.uniform(5, 50), 2)
        payment_status = random.choice(['payé', 'échoué'])
        sql_insert_reservation = f"""
        INSERT INTO ParkingReservation (user_id, parking_spot_id, start_time, end_time, amount_paid, payment_status)
        VALUES ({user_id}, {parking_spot_id}, '{start_time}', '{end_time}', {amount_paid}, '{payment_status}');
        """
        execute_sql('parking_db', sql_insert_reservation)

    for _ in range(20):
        reservation_id = random.randint(1, 20)
        payment_method = random.choice(['carte bancaire', 'PayPal'])
        payment_date = fake.date_time_this_year()
        amount = round(random.uniform(5, 50), 2)
        sql_insert_payment = f"""
        INSERT INTO Payment (reservation_id, payment_method, payment_date, amount)
        VALUES ({reservation_id}, '{payment_method}', '{payment_date}', {amount});
        """
        execute_sql('parking_db', sql_insert_payment)

    print("Les données de test ont été insérées avec succès.")

if __name__ == "__main__":
    clear_existing_data()
    insert_test_data()

import subprocess
from werkzeug.security import generate_password_hash

config = {
    'user': 'root',
    'password': 'rootroot',
    'host': 'it-chaircapgemini.c1q8gu2s6pm0.eu-north-1.rds.amazonaws.com',
    'port': '3306'
}


mysql_executable_path = "mysql"

def drop_database(database_name):
    command = [
        mysql_executable_path,
        '-u', config['user'],
        '-p' + config['password'],
        '-h', config['host'],
        '-P', config['port'],
        '-e', f"DROP DATABASE IF EXISTS {database_name};"
    ]
    subprocess.run(command, check=True)
    print(f"Base de données '{database_name}' supprimée si elle existait.")

def create_database(database_name):
    command = [
        mysql_executable_path,
        '-u', config['user'],
        '-p' + config['password'],
        '-h', config['host'],
        '-P', config['port'],
        '-e', f"""
        CREATE DATABASE {database_name}
        CHARACTER SET utf8mb4
        COLLATE utf8mb4_general_ci;
        """
    ]
    subprocess.run(command, check=True)
    print(f"Base de données '{database_name}' recréée avec charset utf8mb4 et collation utf8mb4_general_ci.")

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

if __name__ == "__main__":
    drop_database('parking_db')
    create_database('parking_db')

    create_role_table_query = """
    CREATE TABLE IF NOT EXISTS Role (
        id INT AUTO_INCREMENT PRIMARY KEY,
        role_name VARCHAR(50) NOT NULL UNIQUE
    ) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
    """
    execute_sql('parking_db', create_role_table_query)

    insert_roles_query = """
    INSERT INTO Role (id, role_name) VALUES (1, 'admin'), (2, 'agent'), (3, 'usager');
    """
    execute_sql('parking_db', insert_roles_query)

    create_user_table_query = """
    CREATE TABLE IF NOT EXISTS User (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(80) NOT NULL,
        email VARCHAR(120) NOT NULL UNIQUE,
        password_hash VARCHAR(255) NOT NULL,
        role_id INT NOT NULL,
        active BOOLEAN NOT NULL DEFAULT TRUE,
        FOREIGN KEY (role_id) REFERENCES Role(id) ON DELETE CASCADE
    ) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
    """
    execute_sql('parking_db', create_user_table_query)


    admin_password_hash = generate_password_hash('admin11')

    insert_admin_user_query = f"""
    INSERT INTO User (username, email, password_hash, role_id, active) 
    VALUES ('admin', 'admin@admin.fr', '{admin_password_hash}', 1, TRUE);
    """
    execute_sql('parking_db', insert_admin_user_query)

    print("Base de données, tables, rôles et utilisateur admin créés avec succès.")


    create_vehicle_type_table_query = """
    CREATE TABLE IF NOT EXISTS VehicleType (
        id INT AUTO_INCREMENT PRIMARY KEY,
        type_name VARCHAR(50) NOT NULL UNIQUE
    ) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
    """
    execute_sql('parking_db', create_vehicle_type_table_query)


    create_vehicle_table_query = """
    CREATE TABLE IF NOT EXISTS Vehicle (
        id INT AUTO_INCREMENT PRIMARY KEY,
        license_plate VARCHAR(20) NOT NULL UNIQUE, 
        owner_id INT NOT NULL, 
        vehicle_type_id INT NULL, 
        FOREIGN KEY (owner_id) REFERENCES User(id) ON DELETE CASCADE,
        FOREIGN KEY (vehicle_type_id) REFERENCES VehicleType(id) ON DELETE SET NULL
    ) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
    """
    execute_sql('parking_db', create_vehicle_table_query)

    create_parking_spot_table_query = """
    CREATE TABLE IF NOT EXISTS ParkingSpot (
        id INT AUTO_INCREMENT PRIMARY KEY,
        spot_number VARCHAR(10) NOT NULL UNIQUE,  
        status ENUM('libre', 'occupée') NOT NULL,  
        vehicle_id INT,  
        spot_type ENUM('normale', 'handicapé', '2 roues', 'électrique') NOT NULL,  
        FOREIGN KEY (vehicle_id) REFERENCES Vehicle(id) ON DELETE SET NULL
    ) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
    """
    execute_sql('parking_db', create_parking_spot_table_query)

    create_parking_reservation_table_query = """
    CREATE TABLE IF NOT EXISTS ParkingReservation (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,  
        parking_spot_id INT NOT NULL,  
        start_time DATETIME NOT NULL,  
        end_time DATETIME NOT NULL,  
        amount_paid DECIMAL(10, 2) NOT NULL,  
        payment_status ENUM('payé', 'échoué') NOT NULL,  
        FOREIGN KEY (user_id) REFERENCES User(id) ON DELETE CASCADE,
        FOREIGN KEY (parking_spot_id) REFERENCES ParkingSpot(id) ON DELETE CASCADE
    ) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
    """
    execute_sql('parking_db', create_parking_reservation_table_query)

    create_payment_table_query = """
    CREATE TABLE IF NOT EXISTS Payment (
        id INT AUTO_INCREMENT PRIMARY KEY,
        reservation_id INT NOT NULL,  
        payment_method ENUM('carte bancaire', 'PayPal') NOT NULL,  
        payment_date DATETIME NOT NULL,  
        amount DECIMAL(10, 2) NOT NULL,  
        FOREIGN KEY (reservation_id) REFERENCES ParkingReservation(id) ON DELETE CASCADE
    ) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
    """
    execute_sql('parking_db', create_payment_table_query)

    print("Base de données et tables supplémentaires créées avec succès.")

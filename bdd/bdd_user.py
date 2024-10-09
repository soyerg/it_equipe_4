import sqlite3




# Function to create the database and users table
def create_database( name = 'users.db'):

    # Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect(name )
    cursor = conn.cursor()

    # Create the users table with unique email constraint
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()




# Function to disconnect from the database
def disconnect_from_database(conn):
    conn.close()




# Function to add a new user
def add_user(email, password, bdd='users.db'):
    conn = sqlite3.connect(bdd)
    cursor = conn.cursor()
    try:
        cursor.execute('''
        INSERT INTO users (email, password) VALUES (?, ?)
        ''', (email, password))
        conn.commit()
        print("User added successfully.")
    except sqlite3.IntegrityError:
        print("Error: Email already exists.")
    disconnect_from_database(conn)

# Function to retrieve a user's password by email
def get_password_by_email(email, bdd='users.db'):
    conn = sqlite3.connect(bdd)
    cursor = conn.cursor()
    cursor.execute('''
    SELECT password FROM users WHERE email = ?
    ''', (email,))
    result = cursor.fetchone()
    disconnect_from_database(conn)
    if result:
        return result[0]
    else:
        return None
    
    # Function to delete a user by email
def delete_user_by_email(email, bdd='users.db'):
        conn = sqlite3.connect(bdd)
        cursor = conn.cursor()
        cursor.execute('''
        DELETE FROM users WHERE email = ?
        ''', (email,))
        conn.commit()
        if cursor.rowcount > 0:
            print("User deleted successfully.")
        else:
            print("Error: Email not found.")
        disconnect_from_database(conn)

create_database()

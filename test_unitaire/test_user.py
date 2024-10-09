import sys
import sqlite3
import os



# Ajouter le chemin du répertoire parent pour que le module bdd_user soit accessible
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'bdd')))

from bdd_user import create_database, add_user, get_password_by_email,delete_user_by_email


create_database("test.db")

def cleanup():
    if os.path.exists("test.db"):
        os.remove("test.db")




# Test create_database function
# Ajouter le chemin du répertoire parent pour que le module bdd_user soit accessible

def test_create_database():
    
    # Create database
    create_database("test.db")
    
    # Check if database file is created
    assert os.path.exists("test.db"), "Database file was not created"
    
    # Cleanup after test
    print("test_create_database ok.")
    cleanup()

def test_add_user():
    # Setup
    create_database("test.db")
    
    # Add user
    add_user( "test@example.com", "password123", bdd="test.db")
    
    # Verify user is added
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", ("test@example.com",))
    user = cursor.fetchone()
    conn.close()
    
    assert user is not None, "User was not added to the database"
    assert user[1] == "test@example.com", "User email does not match"
    assert user[2] == "password123", "User password does not match"
    # Ajouter le chemin du répertoire parent pour que le module bdd_user soit accessible
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'bdd')))
    print("test_add_user ok.")
    cleanup()


def test_get_password_by_email():
        # Setup
        create_database("test.db")
        add_user("test@example.com", "password123", "test.db")
        
        # Get password by email
        password = get_password_by_email( "test@example.com", "test.db")
        
        # Verify password
        assert password == "password123", "Password does not match"
        print("test_get_password_by_email ok.") 
        # Cleanup
        cleanup()

def test_add_duplicate_user():
        # Setup
        create_database("test.db")
        
        # Add first user
        add_user( "test@example.com", "password123", "test.db")
        
        
        add_user("test@example.com", "password456", "test.db")
        
        # Verify only one user is added
        conn = sqlite3.connect("test.db")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users WHERE email = ?", ("test@example.com",))
        count = cursor.fetchone()[0]
        conn.close()
        
        assert count == 1, "Duplicate user was added to the database"
        print("test_add_duplicate_user ok.")
        # Cleanup
        cleanup()

def test_delete_user_by_email():
            # Setup
            create_database("test.db")
            add_user("test@example.com", "password123", "test.db")
            
            # Verify user is added
            conn = sqlite3.connect("test.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE email = ?", ("test@example.com",))
            user = cursor.fetchone()
            assert user is not None, "User was not added to the database"
            
            # Delete user
            delete_user_by_email("test@example.com", "test.db")
            
            # Verify user is deleted
            cursor.execute("SELECT * FROM users WHERE email = ?", ("test@example.com",))
            user = cursor.fetchone()
            conn.close()
            print("test_delete_user_by_email ok.")
            assert user is None, "User was not deleted from the database"
            
            # Cleanup
            cleanup()



# Run tests
test_create_database()
test_add_user()
test_get_password_by_email()
test_add_duplicate_user()
test_delete_user_by_email()
cleanup()


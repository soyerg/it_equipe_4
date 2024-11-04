from flask import url_for
from werkzeug.security import generate_password_hash
from models import User

def test_register(client, db_session):
    """Test de l'inscription d'un nouvel utilisateur."""
    response = client.post('/register', data={
        'username': 'testuser',
        'email': 'testuser@test.com',
        'password': 'password123'
    })
    assert response.status_code == 302  # Redirection après inscription
    assert User.query.filter_by(email='testuser@test.com').first() is not None

def test_login(client, db_session):
    """Test de connexion d'un utilisateur existant."""
    user = User(username="existinguser", email="existing@test.com", password_hash=generate_password_hash("password123"))
    db_session.add(user)
    db_session.commit()

    response = client.post('/login', data={
        'email': 'existing@test.com',
        'password': 'password123'
    })
    assert response.status_code == 302  # Redirection vers le tableau de bord
    assert b"Email ou mot de passe incorrect" not in response.data

def test_logout(client, db_session):
    """Test de déconnexion d'un utilisateur."""
    response = client.get('/logout')
    assert response.status_code == 302  # Redirection après déconnexion

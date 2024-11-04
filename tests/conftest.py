import pytest
from app import app as flask_app
from models import db
from utils.email_utils import send_email
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database, drop_database

# Configurer la base de données de test
TEST_DATABASE_URI = 'sqlite:///test_db.sqlite'

@pytest.fixture(scope='session')
def app():
    """Fixture pour configurer une application Flask en mode test."""
    flask_app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": TEST_DATABASE_URI,
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    })

    # Initialiser la base de données de test
    engine = create_engine(TEST_DATABASE_URI)
    if not database_exists(engine.url):
        create_database(engine.url)

    with flask_app.app_context():
        db.init_app(flask_app)
        db.create_all()

    yield flask_app

    # Supprimer la base de données de test après les tests
    with flask_app.app_context():
        db.session.remove()
        db.drop_all()
    if database_exists(engine.url):
        drop_database(engine.url)

@pytest.fixture(scope='function')
def client(app):
    """Fixture pour un client de test Flask."""
    return app.test_client()

@pytest.fixture(scope='function')
def db_session(app):
    """Fixture pour la session de base de données."""
    with app.app_context():
        db.create_all()
    yield db.session
    db.session.rollback()
    db.drop_all()

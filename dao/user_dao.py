# dao/user_dao.py
from models import db, User
from utils.errors import RecordNotFoundError


class UserDAO:
    @staticmethod
    def get_user_by_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def get_user_by_id(user_id):
        user = User.query.get(user_id)
        if not user:
            raise RecordNotFoundError("Utilisateur non trouvé")
        return user

    @staticmethod
    def create_user(username, email, password_hash, role_id):
        new_user = User(username=username, email=email, password_hash=password_hash, role_id=role_id)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @staticmethod
    def update_user(user_id, username=None, email=None, role_id=None):
        user = User.query.get(user_id)
        if not user:
            raise RecordNotFoundError("Utilisateur non trouvé")

        if username:
            user.username = username
        if email:
            user.email = email
        if role_id:
            user.role_id = role_id

        db.session.commit()
        return user

    @staticmethod
    def delete_user(user_id):
        user = User.query.get(user_id)
        if not user:
            raise RecordNotFoundError("Utilisateur non trouvé")
        db.session.delete(user)
        db.session.commit()

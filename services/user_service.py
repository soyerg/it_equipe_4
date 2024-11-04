# services/user_service.py
from dao.user_dao import UserDAO
from werkzeug.security import generate_password_hash, check_password_hash
from utils.errors import UserNotFoundError, DuplicateEmailError


class UserService:
    @staticmethod
    def get_user_by_email(email):
        user = UserDAO.get_user_by_email(email)
        if not user:
            raise UserNotFoundError("Utilisateur non trouvé avec cet email")
        return user

    @staticmethod
    def create_user(username, email, password, role_id):
        if UserDAO.get_user_by_email(email):
            raise DuplicateEmailError("Cet email est déjà enregistré")

        password_hash = generate_password_hash(password)
        return UserDAO.create_user(username, email, password_hash, role_id)

    @staticmethod
    def verify_password(user, password):
        return check_password_hash(user.password_hash, password)

    @staticmethod
    def update_user(user_id, username=None, email=None, role_id=None):
        return UserDAO.update_user(user_id, username, email, role_id)

    @staticmethod
    def delete_user(user_id):
        return UserDAO.delete_user(user_id)

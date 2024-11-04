# dao/role_dao.py
from models import db, Role
from utils.errors import RecordNotFoundError


class RoleDAO:
    @staticmethod
    def get_role_by_id(role_id):
        role = Role.query.get(role_id)
        if not role:
            raise RecordNotFoundError("Rôle non trouvé")
        return role

    @staticmethod
    def create_role(role_name):
        new_role = Role(role_name=role_name)
        db.session.add(new_role)
        db.session.commit()
        return new_role

    @staticmethod
    def update_role(role_id, role_name):
        role = Role.query.get(role_id)
        if not role:
            raise RecordNotFoundError("Rôle non trouvé")

        role.role_name = role_name
        db.session.commit()
        return role

    @staticmethod
    def delete_role(role_id):
        role = Role.query.get(role_id)
        if not role:
            raise RecordNotFoundError("Rôle non trouvé")
        db.session.delete(role)
        db.session.commit()

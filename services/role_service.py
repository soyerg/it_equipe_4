# services/role_service.py
from dao.role_dao import RoleDAO
from utils.errors import RoleNotFoundError, DuplicateRoleError

class RoleService:
    @staticmethod
    def get_role_by_id(role_id):
        role = RoleDAO.get_role_by_id(role_id)
        if not role:
            raise RoleNotFoundError("Rôle non trouvé")
        return role

    @staticmethod
    def create_role(role_name):
        if RoleDAO.get_role_by_name(role_name):
            raise DuplicateRoleError("Ce rôle existe déjà")
        return RoleDAO.create_role(role_name)

    @staticmethod
    def update_role(role_id, role_name):
        return RoleDAO.update_role(role_id, role_name)

    @staticmethod
    def delete_role(role_id):
        return RoleDAO.delete_role(role_id)

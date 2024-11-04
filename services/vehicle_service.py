# services/vehicle_service.py
from dao.vehicle_dao import VehicleDAO
from utils.errors import VehicleNotFoundError, DuplicateVehicleError

class VehicleService:
    @staticmethod
    def get_vehicle_by_id(vehicle_id):
        vehicle = VehicleDAO.get_vehicle_by_id(vehicle_id)
        if not vehicle:
            raise VehicleNotFoundError("Véhicule non trouvé")
        return vehicle

    @staticmethod
    def create_vehicle(license_plate, owner_id, vehicle_type_id):
        if VehicleDAO.get_vehicle_by_license_plate(license_plate):
            raise DuplicateVehicleError("Ce numéro de plaque est déjà enregistré")
        return VehicleDAO.create_vehicle(license_plate, owner_id, vehicle_type_id)

    @staticmethod
    def delete_vehicle(vehicle_id):
        return VehicleDAO.delete_vehicle(vehicle_id)

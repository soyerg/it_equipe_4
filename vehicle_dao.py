# dao/vehicle_dao.py
from models import db, Vehicle
from utils.errors import RecordNotFoundError

class VehicleDAO:
    @staticmethod
    def get_vehicle_by_id(vehicle_id):
        vehicle = Vehicle.query.get(vehicle_id)
        if not vehicle:
            raise RecordNotFoundError("Véhicule non trouvé")
        return vehicle

    @staticmethod
    def create_vehicle(license_plate, owner_id, vehicle_type_id):
        new_vehicle = Vehicle(license_plate=license_plate, owner_id=owner_id, vehicle_type_id=vehicle_type_id)
        db.session.add(new_vehicle)
        db.session.commit()
        return new_vehicle

    @staticmethod
    def delete_vehicle(vehicle_id):
        vehicle = Vehicle.query.get(vehicle_id)
        if not vehicle:
            raise RecordNotFoundError("Véhicule non trouvé")
        db.session.delete(vehicle)
        db.session.commit()

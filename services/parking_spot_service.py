# services/parking_spot_service.py
from dao.parking_spot_dao import ParkingSpotDAO
from utils.errors import ParkingSpotNotFoundError

class ParkingSpotService:
    @staticmethod
    def get_all_spots():
        return ParkingSpotDAO.get_all_spots()

    @staticmethod
    def get_spot_by_id(spot_id):
        spot = ParkingSpotDAO.get_spot_by_id(spot_id)
        if not spot:
            raise ParkingSpotNotFoundError("Place de parking non trouvée")
        return spot

    @staticmethod
    def create_parking_spot(spot_number, status, spot_type, vehicle_id=None):
        return ParkingSpotDAO.create_parking_spot(spot_number, status, spot_type, vehicle_id)

    @staticmethod
    def update_parking_spot(spot_id, status=None, spot_type=None, vehicle_id=None):
        return ParkingSpotDAO.update_parking_spot(spot_id, status, spot_type, vehicle_id)

    @staticmethod
    def delete_parking_spot(spot_id):
        return ParkingSpotDAO.delete_parking_spot(spot_id)

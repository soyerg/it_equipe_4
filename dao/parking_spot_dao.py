# dao/parking_spot_dao.py
from models import db, ParkingSpot
from utils.errors import RecordNotFoundError


class ParkingSpotDAO:
    @staticmethod
    def get_all_spots():
        return ParkingSpot.query.all()

    @staticmethod
    def get_spot_by_id(spot_id):
        spot = ParkingSpot.query.get(spot_id)
        if not spot:
            raise RecordNotFoundError("Place de parking non trouvée")
        return spot

    @staticmethod
    def create_parking_spot(spot_number, status, spot_type, vehicle_id=None):
        new_spot = ParkingSpot(spot_number=spot_number, status=status, spot_type=spot_type, vehicle_id=vehicle_id)
        db.session.add(new_spot)
        db.session.commit()
        return new_spot

    @staticmethod
    def update_parking_spot(spot_id, status=None, spot_type=None, vehicle_id=None):
        spot = ParkingSpot.query.get(spot_id)
        if not spot:
            raise RecordNotFoundError("Place de parking non trouvée")

        if status:
            spot.status = status
        if spot_type:
            spot.spot_type = spot_type
        if vehicle_id:
            spot.vehicle_id = vehicle_id

        db.session.commit()
        return spot

    @staticmethod
    def delete_parking_spot(spot_id):
        spot = ParkingSpot.query.get(spot_id)
        if not spot:
            raise RecordNotFoundError("Place de parking non trouvée")
        db.session.delete(spot)
        db.session.commit()

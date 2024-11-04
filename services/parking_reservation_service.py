# services/parking_reservation_service.py
from dao.parking_reservation_dao import ParkingReservationDAO
from utils.errors import ParkingReservationNotFoundError

class ParkingReservationService:
    @staticmethod
    def get_reservation_by_id(reservation_id):
        reservation = ParkingReservationDAO.get_reservation_by_id(reservation_id)
        if not reservation:
            raise ParkingReservationNotFoundError("Réservation non trouvée")
        return reservation

    @staticmethod
    def create_reservation(user_id, parking_spot_id, start_time, end_time, amount_paid, payment_status):
        return ParkingReservationDAO.create_reservation(user_id, parking_spot_id, start_time, end_time, amount_paid, payment_status)

    @staticmethod
    def delete_reservation(reservation_id):
        return ParkingReservationDAO.delete_reservation(reservation_id)

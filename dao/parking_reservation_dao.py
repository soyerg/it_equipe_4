# dao/parking_reservation_dao.py
from models import db, ParkingReservation
from utils.errors import RecordNotFoundError

class ParkingReservationDAO:
    @staticmethod
    def get_reservation_by_id(reservation_id):
        reservation = ParkingReservation.query.get(reservation_id)
        if not reservation:
            raise RecordNotFoundError("Réservation non trouvée")
        return reservation

    @staticmethod
    def create_reservation(user_id, parking_spot_id, start_time, end_time, amount_paid, payment_status):
        new_reservation = ParkingReservation(
            user_id=user_id, parking_spot_id=parking_spot_id, start_time=start_time,
            end_time=end_time, amount_paid=amount_paid, payment_status=payment_status
        )
        db.session.add(new_reservation)
        db.session.commit()
        return new_reservation

    @staticmethod
    def delete_reservation(reservation_id):
        reservation = ParkingReservation.query.get(reservation_id)
        if not reservation:
            raise RecordNotFoundError("Réservation non trouvée")
        db.session.delete(reservation)
        db.session.commit()

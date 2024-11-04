# dao/payment_dao.py
from models import db, Payment
from utils.errors import RecordNotFoundError

class PaymentDAO:
    @staticmethod
    def get_payment_by_id(payment_id):
        payment = Payment.query.get(payment_id)
        if not payment:
            raise RecordNotFoundError("Paiement non trouvé")
        return payment

    @staticmethod
    def create_payment(reservation_id, payment_method, payment_date, amount):
        new_payment = Payment(reservation_id=reservation_id, payment_method=payment_method, payment_date=payment_date, amount=amount)
        db.session.add(new_payment)
        db.session.commit()
        return new_payment

    @staticmethod
    def delete_payment(payment_id):
        payment = Payment.query.get(payment_id)
        if not payment:
            raise RecordNotFoundError("Paiement non trouvé")
        db.session.delete(payment)
        db.session.commit()

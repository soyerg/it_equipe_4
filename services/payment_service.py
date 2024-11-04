# services/payment_service.py
from dao.payment_dao import PaymentDAO
from utils.errors import PaymentNotFoundError

class PaymentService:
    @staticmethod
    def get_payment_by_id(payment_id):
        payment = PaymentDAO.get_payment_by_id(payment_id)
        if not payment:
            raise PaymentNotFoundError("Paiement non trouvé")
        return payment

    @staticmethod
    def create_payment(reservation_id, payment_method, payment_date, amount):
        return PaymentDAO.create_payment(reservation_id, payment_method, payment_date, amount)

    @staticmethod
    def delete_payment(payment_id):
        return PaymentDAO.delete_payment(payment_id)

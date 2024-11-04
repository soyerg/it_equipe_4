from datetime import datetime, timedelta
from services.parking_reservation_service import ParkingReservationService
from services.parking_spot_service import ParkingSpotService
from services.user_service import UserService
from utils.email_utils import send_email

def check_expired_reservations():
    """Vérifie les réservations expirées et libère les places de parking."""
    now = datetime.utcnow()
    expired_reservations = ParkingReservationService.get_expired_reservations(now)

    for reservation in expired_reservations:
        # Libérer la place de parking
        ParkingSpotService.update_spot_status(reservation.parking_spot_id, "libre")
        # Supprimer la réservation expirée
        ParkingReservationService.delete_reservation(reservation.id)

        # Notifier les agents de la place libérée (exemple)
        agents = UserService.get_all_agents()
        for agent in agents:
            send_email(
                subject="Place de parking libérée",
                recipient=agent.email,
                body=f"La place {reservation.parking_spot_id} est désormais libre après expiration de la réservation."
            )

        # Notifier l'utilisateur de l'expiration de la réservation
        user = UserService.get_user_by_id(reservation.user_id)
        send_email(
            subject="Expiration de votre réservation",
            recipient=user.email,
            body=f"Bonjour {user.username},\n\nVotre réservation pour la place {reservation.parking_spot_id} a expiré."
        )

def notify_near_end_time():
    """Notifie les utilisateurs dont la réservation est proche de l'expiration."""
    reminder_time_start = datetime.utcnow() + timedelta(minutes=29, seconds=30)
    reminder_time_end = datetime.utcnow() + timedelta(minutes=30, seconds=30)

    reservations = ParkingReservationService.get_reservations_in_time_range(reminder_time_start, reminder_time_end)

    for reservation in reservations:
        user = UserService.get_user_by_id(reservation.user_id)
        send_email(
            subject="Fin de stationnement proche",
            recipient=user.email,
            body=f"Bonjour {user.username},\n\nVotre stationnement pour la place {reservation.parking_spot_id} se termine bientôt à {reservation.end_time}. Veuillez prolonger si nécessaire."
        )

class DuplicateEmailError(Exception):
    """Raised when attempting to create a user with an already existing email."""
    pass

class UserNotFoundError(Exception):
    """Raised when a user is not found in the database."""
    pass

class DuplicateVehicleError(Exception):
    """Raised when attempting to add a vehicle with an already existing license plate."""
    pass

class ReservationError(Exception):
    """Raised when there is an error related to parking reservation."""
    pass

# Ajoutez d'autres erreurs spécifiques si nécessaire

from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(50), unique=True, nullable=False)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    active = db.Column(db.Boolean, default=True)

    role = db.relationship('Role', backref=db.backref('users', lazy=True))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_active(self):
        return self.active


class ParkingSpot(db.Model):
    __tablename__ = 'parkingspot'
    id = db.Column(db.Integer, primary_key=True)
    spot_number = db.Column(db.String(10), unique=True, nullable=False)
    status = db.Column(db.Enum('libre', 'occupée'), nullable=False, default='libre')
    spot_type = db.Column(db.Enum('normale', 'handicapé', '2 roues', 'électrique'), nullable=False, default='normale')
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'), nullable=True)

    vehicle = db.relationship('Vehicle', backref=db.backref('parked_spots', lazy=True))


class VehicleType(db.Model):
    __tablename__ = 'vehicletype'  # Nom explicite de la table
    id = db.Column(db.Integer, primary_key=True)
    type_name = db.Column(db.String(50), unique=True, nullable=False)



class Vehicle(db.Model):
    __tablename__ = 'vehicle'  # Assurez-vous que le nom de la table est correct
    id = db.Column(db.Integer, primary_key=True)
    license_plate = db.Column(db.String(20), unique=True, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    vehicle_type_id = db.Column(db.Integer, db.ForeignKey('vehicletype.id'), nullable=False)  # Vérifiez que le nom de la table est bien 'vehicletype'

    owner = db.relationship('User', backref=db.backref('vehicles', lazy=True))
    vehicle_type = db.relationship('VehicleType', backref=db.backref('vehicles', lazy=True))


class ParkingReservation(db.Model):
    __tablename__ = 'parkingreservation'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    parking_spot_id = db.Column(db.Integer, db.ForeignKey('parkingspot.id'), nullable=False)
    start_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    amount_paid = db.Column(db.Numeric(10, 2), nullable=False)
    payment_status = db.Column(db.Enum('payé', 'échoué'), nullable=False)

    user = db.relationship('User', backref=db.backref('reservations', lazy=True))
    parking_spot = db.relationship('ParkingSpot', backref=db.backref('reservations', lazy=True))

class Payment(db.Model):
    __tablename__ = 'payment'
    id = db.Column(db.Integer, primary_key=True)
    reservation_id = db.Column(db.Integer, db.ForeignKey('parkingreservation.id'), nullable=False)
    payment_method = db.Column(db.Enum('carte bancaire', 'PayPal'), nullable=False)
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)
    amount = db.Column(db.Numeric(10, 2), nullable=False)

    reservation = db.relationship('ParkingReservation', backref=db.backref('payments', lazy=True))

from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from services.user_service import UserService
from services.role_service import RoleService
from services.parking_spot_service import ParkingSpotService
from services.parking_reservation_service import ParkingReservationService
from services.vehicle_service import VehicleService
from services.scheduler_service import check_expired_reservations, notify_near_end_time
from services.payment_service import PaymentService
from utils.email_utils import send_email
from utils.errors import *
from db_config import get_connection
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Configuration de la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = get_connection('PROD', 'parking_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuration de LoginManager
login_manager = LoginManager(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return UserService.get_user_by_id(user_id)


@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/forgot_password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    email = data.get('email')
    try:
        user = UserService.get_user_by_email(email)
        send_email(
            subject="Votre mot de passe Park & See",
            recipient=email,
            body=f"Bonjour {user.username},\n\nVotre mot de passe est : {user.get_password()}\n\nMerci d'utiliser Park & See !"
        )
        return jsonify({"status": "success", "message": "Le mot de passe a été envoyé à votre adresse e-mail."}), 200
    except UserNotFoundError:
        return jsonify({"status": "error", "message": "Aucun compte trouvé avec cette adresse e-mail."}), 404


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            user = UserService.get_user_by_email(email)
            if UserService.verify_password(user, password):
                login_user(user)
                return redirect(url_for('dashboard'))
            flash('Email ou mot de passe incorrect.')
        except UserNotFoundError:
            flash('Email ou mot de passe incorrect.')
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Vous avez été déconnecté.')
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role_id = 3  # Rôle par défaut pour les usagers
        try:
            UserService.create_user(username, email, password, role_id)
            send_email(
                subject="Bienvenue dans Park & See",
                recipient=email,
                body=f"Bonjour {username},\n\nVotre compte Park & See a été créé avec succès.\n\nCordialement,\nL'équipe Park & See"
            )
            flash('Votre compte a bien été créé. Vous pouvez maintenant vous connecter.', 'success')
            return redirect(url_for('login'))
        except DuplicateEmailError:
            flash('Cet email est déjà enregistré. Veuillez vous connecter.', 'danger')
    return render_template('register.html')


@app.route('/dashboard')
@login_required
def dashboard():
    try:
        if current_user.role_id == 1:
            # Dashboard Admin
            users = UserService.get_all_users()
            roles = RoleService.get_all_roles()
            parking_spots = ParkingSpotService.get_all_spots()
            return render_template('admin_dashboard.html', username=current_user.username, users=users, roles=roles,
                                   parking_spots=parking_spots)

        elif current_user.role_id == 2:
            # Dashboard Agent
            occupied_spots = ParkingSpotService.get_occupied_spots()
            free_spots = ParkingSpotService.get_free_spots()
            return render_template('agent_dashboard.html', username=current_user.username,
                                   occupied_spots=occupied_spots, free_spots=free_spots)

        elif current_user.role_id == 3:
            # Dashboard Usager
            parking_spots = ParkingSpotService.get_all_spots()
            user_vehicles = VehicleService.get_user_vehicles(current_user.id)
            user_reservations = ParkingReservationService.get_user_reservations(current_user.id)
            return render_template('usager_dashboard.html', username=current_user.username, parking_spots=parking_spots,
                                   user_vehicles=user_vehicles, user_reservations=user_reservations)

    except Exception as e:
        flash("Une erreur est survenue lors du chargement du tableau de bord.", "danger")
        print(f"Erreur lors du chargement du tableau de bord : {e}")
    return redirect(url_for('index'))


# Routes pour gestion des utilisateurs, des véhicules, des réservations, etc.
@app.route('/add_vehicle', methods=['POST'])
@login_required
def add_vehicle():
    if current_user.role_id == 3:
        license_plate = request.form.get('license_plate')
        vehicle_type_id = request.form.get('vehicle_type_id')
        try:
            VehicleService.create_vehicle(license_plate, current_user.id, vehicle_type_id)
            flash("Véhicule ajouté avec succès.", "success")
        except DuplicateVehicleError:
            flash("Ce numéro de plaque est déjà enregistré.", "danger")
    else:
        flash("Accès non autorisé.", "danger")
    return redirect(url_for('dashboard'))


@app.route('/reserve_spot/<int:spot_id>', methods=['GET', 'POST'])
@login_required
def reserve_spot(spot_id):
    try:
        if request.method == 'POST':
            vehicle_id = request.form.get('vehicle_id')
            start_date = request.form.get('start_date') + ' ' + request.form.get('start_time')
            end_date = request.form.get('end_date') + ' ' + request.form.get('end_time')
            start_time = datetime.strptime(start_date, '%Y-%m-%d %H:%M')
            end_time = datetime.strptime(end_date, '%Y-%m-%d %H:%M')

            amount_paid = round((end_time - start_time).total_seconds() / 3600, 2)
            ParkingReservationService.create_reservation(current_user.id, spot_id, start_time, end_time, amount_paid,
                                                         'payé')

            send_email(
                subject="Confirmation de réservation",
                recipient=current_user.email,
                body=f"Réservation confirmée pour {start_time} à {end_time}, montant : {amount_paid} €."
            )
            flash(f'Réservation réussie pour {amount_paid} €.', 'success')
        return redirect(url_for('dashboard'))
    except Exception as e:
        flash("Erreur lors de la réservation de la place.", "danger")
        print(f"Erreur lors de la réservation : {e}")
    return render_template('reserve_spot.html', spot_id=spot_id)


# Planification de tâches pour les notifications
def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=check_expired_reservations, trigger="interval", minutes=1)
    scheduler.add_job(func=notify_near_end_time, trigger="interval", minutes=1)
    scheduler.start()


if __name__ == '__main__':
    start_scheduler()
    app.run(debug=True, host='0.0.0.0')

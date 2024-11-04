from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Role, ParkingSpot, ParkingReservation, Vehicle, Payment, VehicleType
from db_config import get_connection
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
app.secret_key = 'supersecretkey'

EMAIL_USER = 'notifscrumtroopers@gmail.com'
EMAIL_PASSWORD = 'djxz rrzt bxeu dcuh'

app.config['SQLALCHEMY_DATABASE_URI'] = get_connection('PROD', 'parking_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    with app.app_context():
        return db.session.get(User, int(user_id))

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('login'))

@app.route('/forgot_password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    email = data.get('email')

    user = User.query.filter_by(email=email).first()
    if user:
        # Envoi de l'email avec le mot de passe
        send_email(
            subject="Votre mot de passe Park & See",
            recipient=email,
            body=f"Bonjour {user.username},\n\nVotre mot de passe est : {user.get_password()}\n\nMerci d'utiliser Park & See !"
        )
        return jsonify({"status": "success", "message": "Le mot de passe a été envoyé à votre adresse e-mail."}), 200
    else:
        return jsonify({"status": "error", "message": "Aucun compte trouvé avec cette adresse e-mail."}), 404


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Email ou mot de passe incorrect.')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Vous avez été déconnecté.')
    return redirect(url_for('login'))

def send_email(subject, recipient, body):
    sender_email = EMAIL_USER
    sender_password = EMAIL_PASSWORD

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, recipient, text)
        server.quit()
        print(f"Email sent to {recipient}")
    except Exception as e:
        print(f"Failed to send email: {e}")
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role_id = 3  # Définir automatiquement le rôle d'usager (ID 3)

        if User.query.filter_by(email=email).first():
            flash('Cet email est déjà enregistré. Veuillez vous connecter.', 'danger')
            return redirect(url_for('login'))
        else:
            new_user = User(username=username, email=email, role_id=role_id)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()

            # Envoyer un email de bienvenue
            send_email(
                subject="Bienvenue dans Park & See",
                recipient=email,
                body=f"Bonjour {username},\n\nVotre compte Park & See a été créé avec succès.\n\nCordialement,\nL'équipe Park & See"
            )

            flash('Votre compte a bien été créé. Vous pouvez maintenant vous connecter.', 'success')
            return redirect(url_for('login'))

    return render_template('register.html')



@app.route('/create_role', methods=['POST'])
@login_required
def create_role():
    if current_user.role_id == 1:
        role_name = request.form['role_name']
        new_role = Role(role_name=role_name)
        db.session.add(new_role)
        db.session.commit()
        flash('Rôle créé avec succès.')
        return redirect(url_for('dashboard'))
    return "Non autorisé", 403

@app.route('/edit_role/<int:role_id>', methods=['POST'])
@login_required
def edit_role(role_id):
    if current_user.role_id == 1:
        role = Role.query.get(role_id)
        if role:
            role.role_name = request.form['role_name']
            db.session.commit()
            flash('Rôle modifié avec succès.')
        return redirect(url_for('dashboard'))
    return "Non autorisé", 403

@app.route('/delete_role/<int:role_id>', methods=['POST'])
@login_required
def delete_role(role_id):
    if current_user.role_id == 1:
        role = Role.query.get(role_id)
        if role:
            db.session.delete(role)
            db.session.commit()
            flash('Rôle supprimé avec succès.')
        return redirect(url_for('dashboard'))
    return "Non autorisé", 403



@app.route('/create_user', methods=['POST'])
@login_required
def create_user():
    if current_user.role_id == 1:
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        role_id = request.form.get('role_id')


        if User.query.filter_by(email=email).first():
            flash('L\'email est déjà utilisé.', 'danger')
        else:
            new_user = User(username=username, email=email, role_id=role_id)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            flash('Utilisateur ajouté avec succès.', 'success')

        return redirect(url_for('dashboard'))
    else:
        flash('Accès non autorisé', 'danger')
        return redirect(url_for('dashboard'))



@app.route('/edit_user/<int:user_id>', methods=['POST'])
@login_required
def edit_user(user_id):
    if current_user.role_id == 1:
        user = User.query.get(user_id)
        if user:
            user.username = request.form.get('username')
            user.email = request.form.get('email')
            user.role_id = request.form.get('role_id')
            db.session.commit()
            flash('Utilisateur modifié avec succès.', 'success')
        else:
            flash('Utilisateur non trouvé.', 'danger')
        return redirect(url_for('dashboard'))
    else:
        flash('Accès non autorisé', 'danger')
        return redirect(url_for('dashboard'))



@app.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if current_user.role_id == 1:
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            flash('Utilisateur supprimé avec succès.', 'success')
        else:
            flash('Utilisateur non trouvé.', 'danger')
        return redirect(url_for('dashboard'))
    else:
        flash('Accès non autorisé', 'danger')
        return redirect(url_for('dashboard'))

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role_id == 1:
        # Code pour l'administrateur
        users = User.query.all()
        roles = Role.query.all()
        parking_spots = ParkingSpot.query.all()
        return render_template(
            'admin_dashboard.html',
            username=current_user.username,
            users=users,
            roles=roles,
            parking_spots=parking_spots
        )

    elif current_user.role_id == 2:
        # Code pour l'agent
        occupied_spots = ParkingSpot.query.filter_by(status='occupée').all()
        free_spots = ParkingSpot.query.filter_by(status='libre').all()
        occupied_count = len(occupied_spots)
        free_count = len(free_spots)

        return render_template(
            'agent_dashboard.html',
            username=current_user.username,
            occupied_spots=occupied_spots,
            free_spots=free_spots,
            occupied_count=occupied_count,
            free_count=free_count,
            datetime=datetime
        )

    elif current_user.role_id == 3:
        # Code pour l'usager
        parking_spots = ParkingSpot.query.all()
        user_vehicles = Vehicle.query.filter_by(owner_id=current_user.id).all()
        user_reservations = ParkingReservation.query.filter_by(user_id=current_user.id).all()
        reserved_spot_ids = [reservation.parking_spot_id for reservation in user_reservations]
        vehicle_types = VehicleType.query.all()

        return render_template(
            'usager_dashboard.html',
            username=current_user.username,
            parking_spots=parking_spots,
            user_vehicles=user_vehicles,
            reserved_spot_ids=reserved_spot_ids,
            user_reservations=user_reservations,
            vehicle_types=vehicle_types
        )

    else:
        return "Invalid role", 403





# Route pour ajouter un véhicule pour l'utilisateur connecté
@app.route('/add_vehicle', methods=['POST'])
@login_required
def add_vehicle():
    if current_user.role_id == 3:  # Vérifie que l'utilisateur est un usager
        license_plate = request.form.get('license_plate')
        vehicle_type_id = request.form.get('vehicle_type_id')

        # Vérifie si le véhicule existe déjà
        existing_vehicle = Vehicle.query.filter_by(license_plate=license_plate).first()
        if existing_vehicle:
            flash("Ce numéro de plaque est déjà enregistré.", "danger")
        else:
            new_vehicle = Vehicle(
                license_plate=license_plate,
                owner_id=current_user.id,
                vehicle_type_id=vehicle_type_id
            )
            db.session.add(new_vehicle)
            db.session.commit()
            flash("Véhicule ajouté avec succès.", "success")

        return redirect(url_for('dashboard'))
    else:
        flash("Accès non autorisé.", "danger")
        return redirect(url_for('dashboard'))

@app.route('/create_parking_spot', methods=['POST'])
@login_required
def create_parking_spot():
    if current_user.role_id == 1:
        spot_number = request.form.get('spot_number')
        status = request.form.get('status')
        spot_type = request.form.get('spot_type')

        if ParkingSpot.query.filter_by(spot_number=spot_number).first():
            flash('Le numéro de place est déjà utilisé.', 'danger')
        else:
            new_spot = ParkingSpot(spot_number=spot_number, status=status, spot_type=spot_type)
            db.session.add(new_spot)
            db.session.commit()
            flash('Place de parking ajoutée avec succès.', 'success')

        return redirect(url_for('dashboard'))
    else:
        flash('Accès non autorisé', 'danger')
        return redirect(url_for('dashboard'))


@app.route('/edit_parking_spot/<int:spot_id>', methods=['POST'])
@login_required
def edit_parking_spot(spot_id):
    if current_user.role_id == 1:
        spot = ParkingSpot.query.get(spot_id)
        if spot:
            spot.spot_number = request.form.get('spot_number')
            spot.status = request.form.get('status')
            spot.spot_type = request.form.get('spot_type')
            db.session.commit()
            flash('Place de parking modifiée avec succès.', 'success')
        else:
            flash('Place de parking non trouvée.', 'danger')

        return redirect(url_for('dashboard'))
    else:
        flash('Accès non autorisé', 'danger')
        return redirect(url_for('dashboard'))



@app.route('/delete_parking_spot/<int:spot_id>', methods=['POST'])
@login_required
def delete_parking_spot(spot_id):
    if current_user.role_id == 1:
        spot = ParkingSpot.query.get(spot_id)
        if spot:
            db.session.delete(spot)
            db.session.commit()
            flash('Place de parking supprimée avec succès.', 'success')
        else:
            flash('Place de parking non trouvée.', 'danger')

        return redirect(url_for('dashboard'))
    else:
        flash('Accès non autorisé', 'danger')
        return redirect(url_for('dashboard'))


@app.route('/reserve_spot/<int:spot_id>', methods=['GET', 'POST'])
@login_required
def reserve_spot(spot_id):
    spot = ParkingSpot.query.get(spot_id)
    if request.method == 'POST':
        if spot and spot.status == 'libre':
            vehicle_id = request.form.get('vehicle_id')  # Peut être None si non sélectionné
            start_date = request.form.get('start_date') + ' ' + request.form.get('start_time')
            end_date = request.form.get('end_date') + ' ' + request.form.get('end_time')
            start_time = datetime.strptime(start_date, '%Y-%m-%d %H:%M')
            end_time = datetime.strptime(end_date, '%Y-%m-%d %H:%M')

            # Calcul du montant automatique (par exemple 1€ par heure)
            total_hours = (end_time - start_time).total_seconds() / 3600
            amount_paid = round(total_hours, 2)

            # Crée une réservation seulement si l'utilisateur confirme le paiement
            new_reservation = ParkingReservation(
                user_id=current_user.id,
                parking_spot_id=spot.id,
                start_time=start_time,
                end_time=end_time,
                amount_paid=amount_paid,
                payment_status='payé'
            )

            spot.status = 'occupée'
            if vehicle_id:  # Vérifie si un véhicule a été sélectionné
                spot.vehicle_id = vehicle_id

            db.session.add(new_reservation)
            db.session.commit()

            # Confirmation d'envoi d'e-mail après le paiement réussi
            send_email(
                subject="Confirmation de réservation de stationnement",
                recipient=current_user.email,
                body=f"Bonjour {current_user.username},\n\nVotre place de parking {spot.spot_number} a été réservée avec succès.\n"
                     f"Détails :\n- Début : {start_time}\n- Fin : {end_time}\n- Montant payé : {amount_paid} €\n"
                     "Merci pour votre réservation.\n\nL'équipe Parking"
            )

            flash(f'La place {spot.spot_number} a été réservée avec succès pour {amount_paid} €.', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Cette place est déjà occupée.', 'danger')
            return redirect(url_for('dashboard'))
    return render_template('reserve_spot.html', spot=spot)


def check_expired_reservations():
    with app.app_context():
        now = datetime.utcnow()
        expired_reservations = ParkingReservation.query.filter(
            ParkingReservation.end_time <= now,
            ParkingReservation.payment_status == 'payé'
        ).all()

        for reservation in expired_reservations:
            parking_spot = db.session.get(ParkingSpot, reservation.parking_spot_id)
            parking_spot.status = 'libre'
            db.session.delete(reservation)
            db.session.commit()

            # Notification pour agent en cas de dépassement de temps
            agents = User.query.filter_by(role_id=2).all()
            for agent in agents:
                send_email(
                    subject="Alerte de dépassement de temps de stationnement",
                    recipient=agent.email,
                    body=f"L'usager {reservation.user.username} a dépassé le temps autorisé de stationnement pour la place {parking_spot.spot_number}."
                )

            # Notification de dépassement pour l'usager
            send_email(
                subject="Dépassement du temps de stationnement",
                recipient=reservation.user.email,
                body=f"Bonjour {reservation.user.username},\n\nLe temps de stationnement pour votre place {parking_spot.spot_number} a été dépassé. Veuillez régulariser votre situation.\n\nL'équipe Parking"
            )


def notify_near_end_time():
    with app.app_context():
        reminder_time_start = datetime.utcnow() + timedelta(minutes=29, seconds=30)
        reminder_time_end = datetime.utcnow() + timedelta(minutes=30, seconds=30)

        reservations = ParkingReservation.query.filter(
            ParkingReservation.end_time.between(reminder_time_start, reminder_time_end),
            ParkingReservation.payment_status == 'payé'
        ).all()

        for reservation in reservations:
            send_email(
                subject="Fin de stationnement proche",
                recipient=reservation.user.email,
                body=f"Bonjour {reservation.user.username},\n\nVotre stationnement pour la place {reservation.parking_spot.spot_number} se termine bientôt à {reservation.end_time}.\n"
                     "Veuillez prolonger votre réservation si nécessaire.\n\nL'équipe Parking"
            )


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=check_expired_reservations, trigger="interval", minutes=1)
    scheduler.add_job(func=notify_near_end_time, trigger="interval", minutes=1)
    scheduler.start()

@app.route('/test_email')
def test_email():
    try:
        send_email(
            subject="Test Email",
            recipient="ericrajii@gmail.com",
            body="This is a test email from your Flask application."
        )
        return "Test email sent!"
    except Exception as e:
        return f"Failed to send test email: {str(e)}"


if __name__ == '__main__':
    start_scheduler()
    app.run(debug=True, host='0.0.0.0')





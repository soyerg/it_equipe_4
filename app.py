from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Role, ParkingSpot, ParkingReservation, Vehicle
from db_config import get_connection
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler


app = Flask(__name__)
app.secret_key = 'supersecretkey'

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


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role_id = request.form['role_id']

        if User.query.filter_by(email=email).first():
            flash('Cet email est déjà enregistré. Veuillez vous connecter.', 'danger')
            return redirect(url_for('login'))
        else:
            new_user = User(username=username, email=email, role_id=role_id)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()

            flash('Votre compte a bien été créé. Vous pouvez maintenant vous connecter.', 'success')
            return redirect(url_for('login'))

    roles = Role.query.filter(Role.id != 1).all()
    return render_template('register.html', roles=roles)


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
        users = User.query.all()
        roles = Role.query.all()
        parking_spots = ParkingSpot.query.all()
        return render_template('admin_dashboard.html', username=current_user.username, users=users, roles=roles, parking_spots=parking_spots)

    elif current_user.role_id == 2:
        occupied_spots = ParkingSpot.query.filter_by(status='occupée').all()
        free_spots = ParkingSpot.query.filter_by(status='libre').all()

        occupied_count = len(occupied_spots)
        free_count = len(free_spots)

        return render_template('agent_dashboard.html',
                               username=current_user.username,
                               occupied_spots=occupied_spots,
                               free_spots=free_spots,
                               occupied_count=occupied_count,
                               free_count=free_count,
                               datetime=datetime)
    elif current_user.role_id == 3:
        parking_spots = ParkingSpot.query.all()
        return render_template('usager_dashboard.html', username=current_user.username, parking_spots=parking_spots)

    else:
        return "Invalid role", 403







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

@app.route('/reserve_spot/<int:spot_id>', methods=['POST'])
@login_required
def reserve_spot(spot_id):
    spot = ParkingSpot.query.get(spot_id)
    if spot and spot.status == 'libre':
        vehicle_id = request.form.get('vehicle_id')
        start_date = request.form.get('start_date') + ' ' + request.form.get('start_time')
        end_date = request.form.get('end_date') + ' ' + request.form.get('end_time')
        start_time = datetime.strptime(start_date, '%Y-%m-%d %H:%M')
        end_time = datetime.strptime(end_date, '%Y-%m-%d %H:%M')

        # Calculer le montant (1€ par heure)
        total_hours = (end_time - start_time).total_seconds() / 3600
        amount_paid = round(total_hours, 2)

        # Créer la réservation
        new_reservation = ParkingReservation(
            user_id=current_user.id,
            parking_spot_id=spot.id,
            start_time=start_time,
            end_time=end_time,
            amount_paid=amount_paid,
            payment_status='payé'
        )

        # Mettre à jour l'état de la place
        spot.status = 'occupée'
        spot.vehicle_id = vehicle_id

        db.session.add(new_reservation)
        db.session.commit()

        flash(f'La place {spot.spot_number} a été réservée avec succès pour {amount_paid} €.', 'success')
    else:
        flash('Cette place est déjà occupée.', 'danger')

    return redirect(url_for('dashboard'))


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

        print(f"Réservations expirées vérifiées à {now}")

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=check_expired_reservations, trigger="interval", minutes=1)
    scheduler.start()

if __name__ == '__main__':
    start_scheduler()
    app.run(debug=True, host='0.0.0.0')





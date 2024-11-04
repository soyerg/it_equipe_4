from datetime import datetime, timedelta
from models import User, ParkingSpot, Vehicle, ParkingReservation
from werkzeug.security import generate_password_hash


def test_reserve_spot(client, db_session):
    """Test de réservation d'une place de parking."""
    user = User(username="testuser", email="testuser@test.com", password_hash=generate_password_hash("password123"))
    db_session.add(user)
    db_session.commit()

    spot = ParkingSpot(spot_number="SP-1", status="libre", spot_type="normale")
    db_session.add(spot)
    db_session.commit()

    client.post('/login', data={'email': 'testuser@test.com', 'password': 'password123'})
    response = client.post(f'/reserve_spot/{spot.id}', data={
        'start_date': (datetime.now()).strftime('%Y-%m-%d'),
        'start_time': '10:00',
        'end_date': (datetime.now() + timedelta(hours=2)).strftime('%Y-%m-%d'),
        'end_time': '12:00'
    })

    reservation = ParkingReservation.query.filter_by(user_id=user.id).first()
    assert response.status_code == 302
    assert reservation is not None
    assert reservation.parking_spot_id == spot.id

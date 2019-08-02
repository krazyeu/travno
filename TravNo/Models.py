from TravNo import db, login_manager
from flask_login import UserMixin
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    iti_code = db.Column(db.String(10), unique=True, nullable=False)
    email = db.Column(db.String(999), nullable=False)
    departure = db.Column(db.String(74), nullable=False)
    arrival = db.Column(db.String(74), nullable=False)
    code = db.Column(db.String(4), nullable=False)

    def __repr__(self):
        return f"User('{self.iti_code}', '{self.email}', '{self.departure}', '{self.arrival}' )"

class Sub_User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    iti_code = db.Column(db.String(10), nullable=False)
    name = db.Column(db.String(10000), nullable=False)
    email = db.Column(db.String(999), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='/Users/D3m0cr0/Downloads/default.png')

    def __repr__(self):
        return f"Sub_User('{self.iti_code}', '{self.email}', '{self.name}', '{self.image_file}' )"

class Info(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    iti_code = db.Column(db.String(10), unique=True, nullable=False)
    start_travel = db.Column(db.DateTime, nullable=False)
    end_travel = db.Column(db.DateTime, nullable=False)
    departure_airport = db.Column(db.String(10000), nullable=False)
    arr_airport = db.Column(db.String(10000), nullable=False)
    pax = db.Column(db.Integer, nullable=False)
    flight_tix = db.Column(db.String(3), nullable=False)
    accommodation = db.Column(db.String(3), nullable=False)
    accom_style = db.Column(db.String(3), nullable=False)

    def __repr__(self):
        return f"Info('{self.iti_code}', '{self.start_travel}', '{self.end_travel}', '{self.departure_airport}', '{self.arr_airport}'," \
               f"Info('{self.flight_tix}', '{self.accommodation}', '{self.accom_style}')"

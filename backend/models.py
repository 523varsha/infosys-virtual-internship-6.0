from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))
    role = db.Column(db.String(20), default='citizen')   # citizen, ngo, authority, admin
    location = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))


class WaterStations(db.Model):
    __tablename__ = "waterstations"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    location = db.Column(db.String(200))
    latitude = db.Column(db.Numeric)
    longitude = db.Column(db.Numeric)
    managed_by = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))



class Reports(db.Model):
    __tablename__ = "reports"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    photo_url = db.Column(db.String(200))
    location = db.Column(db.String(200))
    description = db.Column(db.Text)
    water_source = db.Column(db.String(100))
    status = db.Column(db.String(20), default='pending')   # pending, verified, rejected
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))



class StationReadings(db.Model):
    __tablename__ = "stationreadings"

    id = db.Column(db.Integer, primary_key=True)
    station_id = db.Column(db.Integer, db.ForeignKey('waterstations.id'))
    parameter = db.Column(db.String(50))  # pH, turbidity, DO, lead, arsenic
    value = db.Column(db.Numeric)
    recorded_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))



class Searches(db.Model):
    __tablename__ = "searches"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    parameter = db.Column(db.String(50))  # Region, Country, State, Station Name, Station ID
    value = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    address = db.Column(db.String(255))
    energy_usage = db.Column(db.Float)
    num_cars = db.Column(db.Integer)
    energy_storage = db.Column(db.Float)

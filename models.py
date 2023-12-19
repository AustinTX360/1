from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.Text, nullable=False)
    energy_usage = db.Column(db.Float, nullable=False)
    num_cars = db.Column(db.Integer, nullable=False)
    energy_storage = db.Column(db.Float, nullable=False)

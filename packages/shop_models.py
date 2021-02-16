from datetime import datetime

from packages import db


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(range(5, 51)), nullable=False)
                     # TODO: is it possible -  db.String(range(5, 51)  ????
    description = db.Column(db.String(500))
    price = db.Column(db.Numeric(18, 2), price_positive=True)
    quantity = db.Column(db.Integer, quantity_positive=True)
    image_url = db.Column(db.String)
    category = db.relationship('Category', backref='item')


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String(500))
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))


class QuantityHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    old_quantity = db.Column(db.Integer, old_quantity_positive=True)
    new_quantity = db.Column(db.Integer, new_quantity_positive=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(100), nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    updated_on = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


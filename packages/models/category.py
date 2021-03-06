
from packages import db


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)
    description = db.Column(db.String(500))
    items = db.relationship('Item', backref='category', lazy=True)

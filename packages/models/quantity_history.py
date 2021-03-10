from sqlalchemy.orm import validates
from packages import db
from datetime import datetime


class QuantityHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    old_quantity = db.Column(db.Integer)
    new_quantity = db.Column(db.Integer)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)

    # Attributes Validations:
    @validates('old_quantity')
    def validate_old_quantity(self, key, old_quantity):
        if old_quantity >= 0:
            return old_quantity
        else:
            raise ValueError('Value of old_quantity must be non negative')

    @validates('new_quantity')
    def validate_old_quantity(self, key, new_quantity):
        if new_quantity >= 0:
            return new_quantity
        else:
            raise ValueError('Value of new_quantity must be non negative')
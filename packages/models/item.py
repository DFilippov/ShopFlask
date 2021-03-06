from sqlalchemy.orm import validates

from packages import db


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(500))
    price = db.Column(db.Numeric(18, 2))
    quantity = db.Column(db.Integer)
    image_url = db.Column(db.String)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    quantity_history = db.relationship('QuantityHistory', backref='item', lazy=True, cascade="all, delete-orphan")

    # Attributes Validations:
    @validates('name')
    def validate_name(self, key, name) -> str:
        if len(name) in range(5, 51):
            return name
        else:
            raise ValueError("item's name must be between 5 and 50")

    # TODO: -> str replace with int !!
    @validates('price')
    def validate_price(self, key, price) -> int:
        if float(price) >= 0:
            return price
        else:
            raise ValueError('Price value must be positive number')

    @validates('quantity')
    def validate_quantity(self, key, quantity):
        if int(quantity) >= 0:
            return quantity
        else:
            raise ValueError('Quantity value must be positive number')

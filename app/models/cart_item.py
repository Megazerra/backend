from flask_login import UserMixin
from app import db

class CartItem(UserMixin, db.Model):
    __tablename__ = 'cart_items'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(150), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, default=1)
    image_url = db.Column(db.String(255))

    def to_dict(self):
        return {
            'id': self.product_id,
            'name': self.name,
            'price': self.price,
            'quantity': self.quantity,
            'imageUrl': self.image_url
        }
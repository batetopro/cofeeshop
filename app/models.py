from app import db


class Customer(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True)
    home_store = db.Column(db.Integer)
    name = db.Column(db.String(120))
    email = db.Column(db.String(120))
    customer_since = db.Column(db.Date)
    loyalty_card_number = db.Column(db.String(12))
    birthdate = db.Column(db.Date)
    gender = db.Column(db.String(1))
    birth_year = db.Column(db.Integer)

    def __repr__(self):
        return '<Customer {}>'.format(self.name)


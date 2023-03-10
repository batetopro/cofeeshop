from app import db


class Staff(db.Model):
    staff_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120))
    last_name = db.Column(db.String(120))
    position = db.Column(db.String(120))
    start_date = db.Column(db.Date)
    location = db.Column(db.String(2))

    def __repr__(self):
        return '<Staff {} {}>'.format(self.first_name, self.last_name)


class SalesOutlet(db.Model):
    sales_outlet_id = db.Column(db.Integer, primary_key=True)
    sales_outlet_type = db.Column(db.String(32))
    store_square_feet = db.Column(db.Integer)
    store_address = db.Column(db.String(64))
    store_city = db.Column(db.String(32))
    store_state_province = db.Column(db.String(2))
    store_telephone = db.Column(db.String(16))
    store_postal_code = db.Column(db.String(10))
    store_longitude = db.Column(db.Float(precision=9, decimal_return_scale=6))
    store_latitude = db.Column(db.Float(precision=9, decimal_return_scale=6))
    manager = db.Column(db.Integer, db.ForeignKey('staff.staff_id'), nullable=True)
    neighborhood = db.Column(db.String(32))

    def __repr__(self):
        return '<SalesOutlet {}>'.format(self.store_address)


class Customer(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True)
    home_store = db.Column(db.Integer, db.ForeignKey('sales_outlet.sales_outlet_id'))
    name = db.Column(db.String(120))
    email = db.Column(db.String(120))
    customer_since = db.Column(db.Date)
    loyalty_card_number = db.Column(db.String(12))
    birthdate = db.Column(db.Date)
    gender = db.Column(db.String(1))
    birth_year = db.Column(db.Integer)

    def __repr__(self):
        return '<Customer {}>'.format(self.name)


class Product(db.Model):
    product_id = db.Column(db.Integer, primary_key=True)
    product_group = db.Column(db.String(120))
    product_category = db.Column(db.String(120))
    product_type = db.Column(db.String(120))
    product = db.Column(db.String(120))
    product_description = db.Column(db.Text)
    unit_of_measure = db.Column(db.String(32))
    current_wholesale_price = db.Column(db.Float(decimal_return_scale=2))
    current_retail_price = db.Column(db.Float(decimal_return_scale=2))
    tax_exempt_yn = db.Column(db.String(1))
    promo_yn = db.Column(db.String(1))
    new_product_yn = db.Column(db.String(1))

    def __repr__(self):
        return '<Product {}>'.format(self.product)


class Receipt(db.Model):
    __table_args__ = (
        db.PrimaryKeyConstraint('transaction_id', 'transaction_date', 'transaction_time', 'sales_outlet_id'),
    )

    transaction_id = db.Column(db.Integer)
    transaction_date = db.Column(db.Date)
    transaction_time = db.Column(db.Time)
    sales_outlet_id = db.Column(db.Integer, db.ForeignKey('sales_outlet.sales_outlet_id'))
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.staff_id'))
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'))
    instore_yn = db.Column(db.String(1))
    order = db.Column(db.SmallInteger)
    line_item_id = db.Column(db.SmallInteger)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'))
    quantity = db.Column(db.Integer)
    line_item_amount = db.Column(db.Float(decimal_return_scale=2))
    unit_price = db.Column(db.Float(decimal_return_scale=2))
    promo_item_yn = db.Column(db.String(1))



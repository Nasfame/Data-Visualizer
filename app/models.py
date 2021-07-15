from flask_login import UserMixin

from . import db


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    # role = db.Column(db.String(30),nullable=False)


class Product(db.Model):
    __tablename__ = "product"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)

    def __init__(self, name):
        self.name = name


class Distributor(db.Model):
    __tablename__ = "distributor"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)

    def __init__(self, name):
        self.name = name


class Distribution(db.Model):
    __tablename__ = "distribution"
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    distributor_id = db.Column(db.Integer, db.ForeignKey('distributor.id'))
    place = db.Column(db.String(150), nullable=False)
    quantity_sold = db.Column(db.Integer)
    year = db.Column(db.Integer, db.CheckConstraint('year>2000'))

    # products = db.relationship('Product', backref=db.backref('distributors', lazy='dynamic'), lazy='joined')
    distributor = db.relationship('Distributor', lazy='joined')
    product = db.relationship('Product', lazy='joined')

    #

    def __init__(self, p_id, d_id, place, q_sold, year):
        self.product_id = p_id
        self.distributor_id = d_id
        self.place = place
        self.quantity_sold = q_sold
        self.year = year

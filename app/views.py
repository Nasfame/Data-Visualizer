from collections import defaultdict

from flask import Blueprint, request, jsonify
from flask_login import login_required
from icecream import ic

from app.models import Distribution, Product, Distributor
from . import db

views = Blueprint("views", __name__)


@views.route('/place/<place>')
@login_required
def area(place):
    distributors = db.session.query(Distribution).filter(Distribution.place == place).all()
    for i in Distribution.query.all():
        ic(i.__dict__)
    distributor = defaultdict(lambda: [])
    for i in distributors:
        d_name = i.distributor.name
        q_sold = i.quantity_sold
        p_name = i.product.name
        distributor[d_name].append({'name': p_name, 'quantity': q_sold})

    res = {"name": place, "distributor": [{'name': x, 'product': y} for x, y in distributor.items()]}
    return jsonify(res)


@views.route('/product/<product>')
@login_required
def product(product):
    p_id = Product.query.filter_by(name=product).first_or_404("Product missing in the DB").id
    products = db.session.query(Distribution).filter(Distribution.product_id == p_id).all()
    for i in Distribution.query.all():
        ic(i.__dict__)
    places = defaultdict(lambda: [])
    for i in products:
        d_name = i.distributor.name
        q_sold = i.quantity_sold
        place = i.place
        places[d_name].append({'name': place, 'quantity': q_sold})

    res = {"name": product, "distributor": [{'name': x, 'place': y} for x, y in places.items()]}
    return jsonify(res)


@views.route('/distributor/<distributor>')
@login_required
def distributor(distributor):
    d_id = Distributor.query.filter_by(name=distributor).first_or_404("Distributor not found in the DB").id
    products = db.session.query(Distribution).filter(Distribution.distributor_id == d_id).all()
    for i in Distribution.query.all():
        ic(i.__dict__)
    places = defaultdict(lambda: [])
    for i in products:
        place = i.place
        p_name = i.product.name
        q_sold = i.quantity_sold
        places[place].append({'name': p_name, 'quantity': q_sold})

    res = {"name": distributor, "place": [{'name': x, 'product': y} for x, y in places.items()]}
    return jsonify(res)


@views.route('/topN/<distributor>')
@login_required
def topN(distributor):
    d_id = Distributor.query.filter_by(name=distributor).first_or_404("Distributor not found in the DB").id
    products = db.session.query(Distribution).filter(Distribution.distributor_id == d_id).group_by(
        Distribution.place).order_by(Distribution.quantity_sold.desc()).all()
    for i in products:
        ic(i.__dict__)
    places = defaultdict(lambda: [])
    for i in products:
        place = i.place
        p_name = i.product.name
        q_sold = i.quantity_sold
        places[place].append({'name': p_name, 'quantity': q_sold})

    res = {"name": distributor, "place": [{'name': x, 'product': y} for x, y in places.items()]}
    return jsonify(res)


class Temp():
    def __init__(self, id):
        self.id = id


@views.route('/distribution/<place>', methods=['POST'])
@login_required
def distribution(place):
    data = request.json
    p_name, d_name = data.get('product'), data.get('distributor')
    q_sold, yr = data.get('quantity_sold'), data.get('year')
    product = Product.query.filter_by(name=p_name).first()
    distributor = Distributor.query.filter_by(name=d_name).first()
    queries = []

    if product is None:
        queries.append(Product(p_name))
        product = Temp(db.session.query(Product).count() + 1)

    if distributor is None:
        queries.append(Distributor(d_name))
        distributor = Temp(db.session.query(Distributor).count() + 1)
    # distribution = {"product_id": p_id, "distributor_id": d_id, "place": place, "quantity_sold": q_sold, "year": yr}
    queries.append(Distribution(product.id, distributor.id, place, q_sold, yr))
    db.session.add_all(queries)
    db.session.commit()

    return jsonify("Data Register Successfully")

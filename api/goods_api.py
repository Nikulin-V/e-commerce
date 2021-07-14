import json

from flask import Blueprint, request, jsonify

from data import db_session
from data.goods import Goods
from data.types import Type
from tools import generate_id

goods_api = Blueprint('goods-api', __name__)


def check_cost(cost):
    try:
        return float(cost)
    except ValueError:
        return jsonify({
            'title': 'Error',
            'errors': [f'Cost should be a float number']
        })


@goods_api.route('/goods', methods=['POST'])
def create_goods():
    """
    Create product\n
    URL arguments:\n
    sku - product's SKU\n
    name - product's name\n
    type_id - id of product type\n
    type_name - name of product name\n
    cost (float) - product's cost
    """
    db_sess = db_session.create_session()

    sku = request.args.get('sku')
    if not sku:
        sku = request.args.get('SKU')

    name = request.args.get('name')
    type_id = request.args.get('type_id')
    cost = request.args.get('cost')
    check_cost(cost)

    all_skus = list(map(lambda x: str(x[0]), db_sess.query(Goods.SKU).all()))
    if sku in all_skus:
        return jsonify({
            'title': 'Error',
            'errors': [f'The product with SKU {sku} already exists']
        })

    if not type_id:
        type_name = request.args.get('type_name')
        if type_name:
            type_id = db_sess.query(Type.id).filter(Type.name == type_name).first()
            if type_id:
                type_id = type_id[0]
            else:
                type_id = create_type(type_name)

    existing_ids = list(map(lambda x: x[0], db_sess.query(Goods.id).all()))
    identifier = generate_id(existing_ids)

    goods = Goods(
        id=identifier,
        SKU=sku,
        name=name,
        type_id=type_id,
        cost=cost
    )
    db_sess.add(goods)
    db_sess.commit()

    return identifier


@goods_api.route('/goods', methods=['GET'])
def read_goods():
    """
    Get info about products\n
    URL arguments:\n
    all_goods (bool) - returns all goods if 1
    """
    all_goods_flag = request.args.get('all_goods')

    if all_goods_flag:
        return read_all_goods()
    else:
        return read_one_goods()


def read_one_goods():
    """
    URL arguments:\n
    id - product's id\n
    sku - product SKU
    """
    identifier = request.args.get('id')
    sku = request.args.get('sku')

    if identifier or sku:
        goods = get_goods(identifier=identifier, sku=sku)
        goods: Goods
        if goods is None:
            return jsonify({
                'title': 'Error',
                'errors': [f'Product {identifier if identifier else sku} was not found']
            })

        return jsonify({
            'title': 'Info about product',
            'product': {
                'id': goods.id,
                'sku': goods.SKU,
                'name': goods.name,
                'type': get_type_name(goods.type_id),
                'cost': goods.cost
            },
            'errors': []
        })

    return jsonify({
        'title': 'Error',
        'errors': ['Specify the ID or SKU']
    })


def read_all_goods():
    """
    URL arguments:\n
    page (int) - page number of catalog\n
    count (int) - count of goods on page\n
    type - type for sorting\n
    min_cost - minimal cost for sorting\n
    max_cost - maximal cost for sorting\n
    """
    db_sess = db_session.create_session()

    sort_type = request.args.get('type')
    page_id = request.args.get('page')
    if not page_id or not page_id.isdigit():
        page_id = 0
    else:
        page_id = int(page_id) - 1

    min_cost = float(request.args.get('min_cost')) if request.args.get('min_cost') else None
    max_cost = float(request.args.get('max_cost')) if request.args.get('max_cost') else None

    if sort_type:
        if sort_type in list(map(lambda x: x[0], db_sess.query(Type.name).all())):
            if min_cost and max_cost:
                goods = db_sess.query(Goods).filter(Goods.type_id == get_type_id(sort_type),
                                                    Goods.cost > min_cost,
                                                    Goods.cost < max_cost)
            elif min_cost is not None:
                goods = db_sess.query(Goods).filter(Goods.type_id == get_type_id(sort_type),
                                                    Goods.cost > min_cost)
            elif max_cost is not None:
                goods = db_sess.query(Goods).filter(Goods.type_id == get_type_id(sort_type),
                                                    Goods.cost < max_cost)
            else:
                goods = db_sess.query(Goods).filter(Goods.type_id == get_type_id(sort_type))
        else:
            return jsonify({
                'title': 'Error',
                'errors': ['There is no such type']
            })
    else:
        goods = db_sess.query(Goods)

    GOODS_FOR_PAGE = request.args.get('count')
    if not GOODS_FOR_PAGE or not GOODS_FOR_PAGE.isdigit():
        GOODS_FOR_PAGE = 50
    else:
        GOODS_FOR_PAGE = int(GOODS_FOR_PAGE)

    if len(list(goods)) > GOODS_FOR_PAGE and len(list(goods)) > GOODS_FOR_PAGE * page_id:
        goods = goods[GOODS_FOR_PAGE * page_id: GOODS_FOR_PAGE * page_id + GOODS_FOR_PAGE]

    g: Goods
    response = {
        'title': 'Info about products',
        'errors': [],
        'products': [
            {
                'id': g.id,
                'sku': g.SKU,
                'name': g.name,
                'type': get_type_name(g.type_id),
                'cost': g.cost
            }
            for g in goods]
    }

    return json.dumps(response)


@goods_api.route('/goods', methods=['PUT'])
def update_goods():
    """
    Change products' info
    URL arguments:\n
    id - product's id\n
    sku - product's SKU\n
    name - product's name\n
    type_id - id of product type\n
    type_name - name of product name\n
    cost (float) - product's cost
    """
    db_sess = db_session.create_session()

    identifier = request.args.get('id')
    sku = request.args.get('sku')
    name = request.args.get('name')
    type_id = get_type_id()
    cost = request.args.get('cost')
    check_cost(cost)

    if identifier or sku:
        goods = get_goods(identifier, sku)

        goods: Goods
        goods.SKU = sku if sku else goods.SKU
        goods.name = name if name else goods.name
        goods.type_id = type_id if type_id else goods.type_id
        goods.cost = cost if cost else goods.cost

        db_sess.merge(goods)
        db_sess.commit()

        return jsonify({
            'title': 'Message',
            'errors': ['The product has been changed']
        })

    return jsonify({
        'title': 'Error',
        'errors': ['Specify the ID or SKU']
    })


@goods_api.route('/goods', methods=['DELETE'])
def delete_goods():
    """
    Delete product
    URL arguments:\n
    id - product's id\n
    sku - product's SKU
    """
    db_sess = db_session.create_session()

    identifier = request.args.get('id')
    sku = request.args.get('sku')

    if identifier or sku:
        goods = get_goods(db_sess, identifier, sku)

        if not goods:
            return jsonify({
                'title': 'Error',
                'errors': [f'Product {identifier if identifier else sku} was not found']
            })

        db_sess.delete(goods)
        db_sess.commit()
        return jsonify({
            'title': 'Message',
            'errors': ['The product was deleted']
        })

    return jsonify({
        'title': 'Error',
        'errors': ['Specify the ID or SKU']
    })


def get_type_name(identifier):
    return db_session.create_session().query(Type.name).filter(Type.id == identifier).first()[0]


def create_type(type_name):
    db_sess = db_session.create_session()

    existing_t_ids = list(map(lambda x: x[0], db_sess.query(Type.id).all()))
    t = Type(
        id=generate_id(existing_t_ids),
        name=type_name
    )
    db_sess.add(t)
    db_sess.commit()

    return t.id


def get_goods(db_sess=None, identifier=None, sku=None):
    if db_sess is None:
        db_sess = db_session.create_session()

    goods = None
    if identifier:
        goods = db_sess.query(Goods).get(identifier)
    elif sku:
        goods = db_sess.query(Goods).filter(Goods.SKU == sku).first()

    return goods


def get_type_id(type_name=None):
    db_sess = db_session.create_session()
    type_id = request.args.get('type_id')
    if not type_id:
        if type_name is None:
            type_name = request.args.get('type_name')
        if type_name:
            type_id = db_sess.query(Type.id).filter(Type.name == type_name).first()
            if type_id:
                type_id = type_id[0]
            else:
                type_id = create_type(type_name)
    elif type_id not in list(map(lambda x: x[0], db_sess.query(Type.id).all())):
        return None

    return type_id

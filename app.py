import os

from flask import Flask, render_template, request
from flask_mobility import Mobility
from flask_mobility.decorators import mobile_template

from api.goods_api import goods_api, get_type_name
from data import db_session
from data.goods import Goods

app = Flask(__name__)
app.config['SECRET_KEY'] = 'xsolla_e-commerce_secret_key'
Mobility(app)

app.register_blueprint(goods_api, url_prefix='/api')

db_session.global_init('db/goods.sqlite')

port = int(os.environ.get('PORT', 5000))


def main():
    app.run()


@app.route('/')
@app.route('/index')
@mobile_template('{mobile/}index.html')
def index(template):
    db_sess = db_session.create_session()

    goods = db_sess.query(Goods).all()
    g: Goods
    goods_data = [(g.id, g.SKU, g.name, get_type_name(g.type_id), g.cost)
                  for g in goods]

    header_id, sort_up = sorting(goods_data)

    return render_template(template,
                           title='E-commerce',
                           table_headers=['ID', 'SKU', 'Name', 'Type', 'Cost'],
                           goods_data=goods_data,
                           header_id=header_id,
                           sort_up=1 if not sort_up else 0
                           )


def sorting(data):
    sort_up = 0
    if request.args.get('sort_id'):
        header_id = int(request.args.get('sort_id'))
    else:
        header_id = 0
    if request.args.get('sort_up'):
        sort_up = int(request.args.get('sort_up'))

    data.sort(key=lambda x: x[header_id], reverse=True if sort_up else False)

    return header_id, sort_up


if __name__ == '__main__':
    main()

from flask import Flask, render_template
from flask_mobility import Mobility
from flask_mobility.decorators import mobile_template

from api.goods_api import goods_api
from data import db_session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'xsolla_e-commerce_secret_key'
Mobility(app)

app.register_blueprint(goods_api, url_prefix='/api')

db_session.global_init('db/goods.sqlite')


def main():
    app.run()


@app.route('/')
@app.route('/index')
@mobile_template('{mobile/}index.html')
def index(template):
    return render_template(template)


if __name__ == '__main__':
    main()

import json
import unittest

from requests import post, put, get

from data import db_session
from tools import generate_id

db_session.global_init('db/goods.sqlite')


class TestCreateGoods(unittest.TestCase):

    def test_default(self):
        db_sess = db_session.create_session()

        from data.goods import Goods
        new_sku = generate_id(list(map(lambda x: x[0], db_sess.query(Goods.SKU).all())))
        response = post(f'http://127.0.0.1:5000/api/goods?'
                        f'sku={new_sku}&'
                        f'name=Xsolla+T-shirt&'
                        f'type_name=Merch&'
                        f'cost=123').text
        self.assertTrue(response.isalpha())
        self.assertTrue(len(response) == 8)

    def test_bad_type_id(self):
        good_response = '{"errors":["The product with SKU T-shirt Xsolla Size: M already ' \
                        'exists"],"title":"Error"}\n'
        response = post('http://127.0.0.1:5000/api/goods?'
                        'sku=T-shirt+Xsolla+Size:+M&'
                        'name=Xsolla+T-shirt&'
                        'type_id=merch&'
                        'cost=123').text
        self.assertEqual(good_response, response)

    def test_new_type(self):
        db_sess = db_session.create_session()

        from data.types import Type
        new_type_name = generate_id(list(map(lambda x: x[0], db_sess.query(Type.id).all())))
        response = post(f'http://127.0.0.1:5000/api/goods?'
                        f'name=Xsolla+T-shirt&'
                        f'type_name={new_type_name}&'
                        f'cost=1234').text
        self.assertTrue(response.isalpha())
        self.assertTrue(len(response) == 8)


class TestUpdateGoods(unittest.TestCase):

    def test_default(self):
        response = put('http://127.0.0.1:5000/api/goods?'
                       'id=uyesrwzt&'
                       'name=Xsolla+T-shirt&'
                       'type_name=Merch&'
                       'cost=123').text
        good_response = '{"message":["The product has been changed"],' \
                        '"title":"Message"}\n'
        self.assertEqual(response, good_response)

    def test_no_identifier(self):
        response = put('http://127.0.0.1:5000/api/goods?'
                       'name=Xsolla+T-shirt&'
                       'type_name=Merch&'
                       'cost=123').text
        good_response = '{"errors":["Specify the ID or SKU"],"title":"Error"}\n'
        self.assertEqual(response, good_response)

    def test_bad_identifier(self):
        response = put('http://127.0.0.1:5000/api/goods?'
                       'id=12345678&'
                       'name=Xsolla+T-shirt&'
                       'type_name=Merch&'
                       'cost=123').text
        good_response = '{"errors":["Product 12345678 was not found"],"title":"Error"}\n'
        self.assertEqual(response, good_response)


class TestReadGoods(unittest.TestCase):

    def test_default(self):
        response = get('http://127.0.0.1:5000/api/goods?'
                       'id=uyesrwzt').text
        good_response = '{"errors":[],"product":{"cost":123.0,"id":"uyesrwzt","name":"Xsolla ' \
                        'T-shirt","sku":"T-shirt Xsolla Size: M","type":"Merch"},"title":"Info ' \
                        'about product"}\n'
        self.assertEqual(good_response, response)

    def test_no_identifier(self):
        response = get('http://127.0.0.1:5000/api/goods?'
                       'name=Xsolla+T-shirt&'
                       'type_name=Merch&'
                       'cost=123').text
        good_response = '{"errors":["Specify the ID or SKU"],"title":"Error"}\n'
        self.assertEqual(response, good_response)

    def test_bad_identifier(self):
        response = get('http://127.0.0.1:5000/api/goods?'
                       'id=12345678&'
                       'name=Xsolla+T-shirt&'
                       'type_name=Merch&'
                       'cost=123').text
        good_response = '{"errors":["Product 12345678 was not found"],"title":"Error"}\n'
        self.assertEqual(response, good_response)

    def test_many_default(self):
        response = json.dumps(get('http://127.0.0.1:5000/api/goods?'
                                  'all_goods=1').json(), indent=4)
        print(response)

    def test_many_sort_by_type(self):
        response = json.dumps(get('http://127.0.0.1:5000/api/goods?'
                                  'all_goods=1&'
                                  'type=Merch').json(), indent=4)
        print(response)

    def test_many_sort_by_cost(self):
        response = json.dumps(get('http://127.0.0.1:5000/api/goods?'
                                  'all_goods=1&'
                                  'min_cost=5000').json(), indent=4)
        print(response)

    def test_many_sort_by_type_and_cost(self):
        response = json.dumps(get('http://127.0.0.1:5000/api/goods?'
                                  'all_goods=1&'
                                  'type=Game&'
                                  'min_cost=5000&'
                                  'max_cost=8000').json(), indent=4)
        print(response)

    def test_many_bad_type(self):
        response = json.dumps(get('http://127.0.0.1:5000/api/goods?'
                                  'all_goods=1&'
                                  'type=Мерч').json())
        good_response = '{"errors": ["There is no such type"], "title": "Error"}'
        self.assertEqual(good_response, response)


if __name__ == '__main__':
    unittest.main()

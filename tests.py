import json

from requests import get, put, post, delete

###################
# Создание товара #
###################

# Верный запрос
# print(post('http://127.0.0.1:5000/api/goods?sku=Футболка+Xsolla+Размер:+XL&name=Xsolla+T-shirt&type_name=Merch&cost=123').text)

# Неверный запрос (type_id)
# print(post('http://127.0.0.1:5000/api/goods?sku=Футболка+Xsolla+Размер:+M&name=Xsolla+T-shirt&type_id=merch&cost=123').text)

# Автоматическое добавление нового типа
# print(put('http://127.0.0.1:5000/api/goods?sku=Футболка+Xsolla+Размер:+M&name=Xsolla+T-shirt&type_name=Souvenir&cost=1234').text)

####################
# Изменение товара #
####################

# Верный запрос
# print(put('http://127.0.0.1:5000/api/goods?id=mdaylsfu&sku=Футболка+Xsolla+Размер:+M&name=Xsolla+T-shirt&type_name=Merch&cost=1234').text)

# Неверный запрос (type_id)
# print(put('http://127.0.0.1:5000/api/goods?id=mdaylsfu&sku=Футболка+Xsolla+Размер:+M&name=Xsolla+T-shirt&type_id=Merch&cost=1234').text)

# Автоматическое добавление нового типа
# print(put('http://127.0.0.1:5000/api/goods?id=mdaylsfu&sku=Футболка+Xsolla+Размер:+M&name=Xsolla+T-shirt&type_name=Souvenir&cost=1234').text)

###################
# Удаление товара #
###################

# Верный запрос
# print(delete('http://127.0.0.1:5000/api/goods?id=asggfdsf').text)
# print(delete('http://127.0.0.1:5000/api/goods?sku=Футболка Xsolla Размер: XL').text)

# Неверный запрос (id)
# print(delete('http://127.0.0.1:5000/api/goods?id=asggfdsf').text)
# print(delete('http://127.0.0.1:5000/api/goods?sku=asggfdsf').text)

#################################
# Получение информации о товаре #
#################################

# Верный запрос
# print(get('http://127.0.0.1:5000/api/goods?id=mdaylsfu').text)
# print(get('http://127.0.0.1:5000/api/goods?sku=Футболка+Xsolla+Размер:+M').text)

# Неверный запрос (неверные id и sku)
# print(get('http://127.0.0.1:5000/api/goods?sku=fdaylsfu').text)
# print(get('http://127.0.0.1:5000/api/goods?id=Футболка+Xsolla+Размер:+M').text)

##################################
# Получение информации о товарах #
##################################

# Верный запрос
# print(json.dumps(get('http://127.0.0.1:5000/api/goods?all_goods=1').json(), indent=4))
# print(json.dumps(get('http://127.0.0.1:5000/api/goods?all_goods=1&type=Merch').json(), indent=4))
# print(json.dumps(get('http://127.0.0.1:5000/api/goods?all_goods=1&type=Game&min_cost=5000').json(),
#                  indent=4))
# print(json.dumps(get('http://127.0.0.1:5000/api/goods?all_goods=1&type=Game&max_cost=5000').json(),
#                  indent=4))
# print(json.dumps(get('http://127.0.0.1:5000/api/goods?all_goods=1&type=Game&min_cost=5000'
#                      '&max_cost=8000').json(), indent=4))
# print(json.dumps(get('http://127.0.0.1:5000/api/goods?all_goods=1&type=Game&min_cost=15000').json(),
#                  indent=4))

# Неверный запрос
# print(json.dumps(get('http://127.0.0.1:5000/api/goods?all_goods=1&type=Мерч').json(), indent=4))

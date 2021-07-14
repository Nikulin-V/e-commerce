# REST API documentation

### Prefix: `/api/goods`
### Example: `https://hostname.com/api/goods`


## Methods
> [POST > Create product](#POST)\
> [PUT > Update product](#PUT)\
> [DELETE > Delete product](#DELETE)\
> [GET > Read product](#GET)
---

### <a id="POST" style="color: grey">POST:</a> Create product

URL arguments:\
No required

`sku` - product's SKU\
`name` - product's name\
`type_id` - id of product type\
`type_name` - name of product name\
`cost` - product's cost (float)

###### returns `new product's id`

---

### <a id="PUT" style="color: grey">PUT:</a> Update product
URL arguments:\
Required: `id or sku`

`id` - product's id (8 lowercase letters)\
`sku` - product's SKU\
`name` - product's name\
`type_id` - id of product type\
`type_name` - name of product name\
`cost` - product's cost (float)

---

### <a id="DELETE" style="color: grey">DELETE:</a> Delete product
URL arguments:\
Required: `id or sku`

`id` - product's id (8 lowercase letters)\
`sku` - product's SKU

---

### <a id="GET" style="color: grey">GET:</a> Read product
URL arguments:\
No required

`all_goods` - returns catalog if 1 else product

---

###### Catalog:

URL arguments:\
No required

`page` - page number of catalog (int)\
`count` - count of products on page (int)\
`type` - type for sorting\
`min_cost` - minimal cost for sorting (float)\
`max_cost` - maximal cost for sorting (float)

###### returns
```json
{
    "title": "Info about products",
    "errors": [],
    "products": [
        {
            "id": "product1_id",
            "sku": "product1_sku",
            "name": "product1_name",
            "type": "product1_type",
            "cost": 1234.0
        },
        {
            "id": "product2_id",
            "sku": "product2_sku",
            "name": "product2_name",
            "type": "product2_type",
            "cost": 5678.0
        }
    ]
}
```

---

###### Product:

URL arguments:\
Required: `id or sku`

`id` - product's id (8 lowercase letters)\
`sku` - product's SKU

###### returns
```json
{
    "title": "Info about product",
    "errors": [],
    "product": {
        "id": "product1_id",
        "sku": "product1_sku",
        "name": "product1_name",
        "type": "product1_type",
        "cost": 1234.0
    }
}
```
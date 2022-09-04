from copy import deepcopy
from msilib.schema import tables
import requests
from http.client import OK
import pandas as panda
import csv
import requests
import json
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
url = 'https://www.fugughouse.com/products.json?limit=1000&page=1'
def getData():
    req = requests.get(url,headers={'User-Agent': USER_AGENT})
    if req.status_code == OK:
        return req.json()['products']


def cross_join(left, right):
    new_rows = [] if right else left
    for left_row in left:
        for right_row in right:
            temp_row = deepcopy(left_row)
            for key, value in right_row.items():
                temp_row[key] = value
            new_rows.append(deepcopy(temp_row))
    return new_rows

def json_to_dataframe(data_in):
    def flatten_json(data, prev_heading=''):
        if isinstance(data, dict):
            rows = [{}]
            for key, value in data.items():
                rows = cross_join(rows, flatten_json(value, prev_heading + '.' + key))
        elif isinstance(data, list):
            rows = []
            for item in data:
                [rows.append(elem) for elem in flatten_list(flatten_json(item, prev_heading))]
        else:
            rows = [{prev_heading[1:]: data}]
        return rows

    return panda.DataFrame(flatten_json(data_in))
def flatten_list(data):
    for elem in data:
        if isinstance(elem, list):
            yield from flatten_list(elem)
        else:
            yield elem
def getProducts():
    products = getData()
    while products:
        for product in products:
            title = product['title']
            handle = product['handle']
            description= product['body_html']
            vendor = product['vendor']
            product_type = product['product_type']
            tags = product['tags']
            for tag in tags:
                tag_data=tag
            for image in product['images']:
                src = image['src']
                position = image['position']
            for variant in product['variants']:
                price = variant["price"]
                sku= variant["sku"]
                grams= variant["grams"]
                taxable= variant["taxable"]
                requires_shipping= variant["requires_shipping"]
                compare_at_price= variant["compare_at_price"]
                position= variant["position"]
                available = variant["available"]
                featured_image= variant["featured_image"]
    productDatas = {
                'Title': title.strip(),
                'Handle': handle.strip(),
                'Body(Description)': description.strip(),
                'Vendor': vendor.strip(),
                'Product Type': product_type,
                'Tags': tag_data.strip(),
                'Image Src': src.strip(),
                'Image Position': position,
                'Price': price,
                'SKU': sku,
                'Grams': grams,
                'Taxable': taxable,
                'Requires Shipping': requires_shipping,
                'Compare At Price': compare_at_price,
                'Available': available
        }
    return productDatas
print(getProducts())
results =[]
for product in getProducts():
    results.append(product)
# df = json_to_dataframe(data)
# df.to_csv('audaciahome.com-update-products.csv')
# print('saved to file')
with open('product.csv', 'w', encoding='utf8', newline='') as f:
    writer =csv.DictWriter(f, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)
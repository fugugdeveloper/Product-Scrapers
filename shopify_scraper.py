from copy import deepcopy
from http.client import OK
from math import prod
from turtle import width
import requests
import pandas as pandas
import sys
import csv
import json
import time
import urllib.request
from urllib.error import HTTPError
from optparse import OptionParser

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
#url = 'https://grillscapes.com/products.json?limit=6000&page=2'
url ='https://www.ambienthomeus.com/products.json?page=5'
#url ='https://starfiredirect.com/products.json?limit=2589'
#url = 'https://homeoutletdirect.com/products.json?limit=7677&page=1'



def getData():
    req = requests.get(url,headers={'User-Agent': USER_AGENT})
    if req.status_code == OK:
        return req.json()['products']


def getProducts():
    page = 1
    products = getData()
    while products:
        for product in products:
            title = product['title']
            product_type = product['product_type']
            product_handle = product['handle']
            product_vendor = product['vendor']
            product_tags = [str(v) for v in product['tags']]

            def get_image(variant_id):
                images = product['images']
                for i in images:
                    k = [str(v) for v in i['variant_ids']]
                    if str(variant_id) in k:
                        return i['src']

                return ''

            for i, variant in enumerate(product['variants']):
                price = variant['price']
                grams = variant['grams']
                featured_image = get_image(variant['id'])
                compare_at_price = variant['compare_at_price']
                position = variant['position']
                requires_shipping = variant['requires_shipping']
                taxable = variant['taxable']
                option1_value = variant['option1'] or ''
                option2_value = variant['option2'] or ''
                option3_value = variant['option3'] or ''
                option_value = ' '.join([option1_value, option2_value,
                                         option3_value]).strip()
                sku = variant['sku']
                main_image_src = ''
                if product['images']:
                    main_image_src = product['images'][0]['src']

                image_src = get_image(variant['id']) or main_image_src
                stock = 'Yes'
                if not variant['available']:
                    stock = 'No'

                row = {'handle': product_handle,
                       'sku': sku,
                       'product_type': product_type,
                       'title': title,
                       'vendor': product_vendor,
                       'tags': product_tags,
                       'option_value': option_value,
                       'price': price,
                       'stock': stock,
                       'grams': grams,
                       'compare_at_price': compare_at_price,
                       'position': position,
                       'requires_shipping': requires_shipping,
                       'taxable': taxable,
                       'option1_value': option1_value,
                       'option2_value': option2_value,
                       'option3_value': option3_value,
                       'featured_image': featured_image,
                       'body': str(product['body_html']),
                       'variant_id': str(variant['id']),
                       'image_src': image_src
                       }
                for k in row:
                    row[k] = str(row[k]) if row[k] else ''
                yield row

        page += 1
        products = getData()


def extractProducts(url, path):
    with open(path, "w", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(['Handle', 'Variant SKU', 'Title',
                         'Product Type', 
                         'Vendor', 
                         'Body (HTML)',
                         'Tags',
                         'Option Values', 
                         'Variant Grams',
                         'Variant In Stock',
                         'Variant Price',
                         'Variant Compare At Price',
                         'Variant Requires Shipping',
                         'Variant Taxable',
                         'Image Src'])
        seen_variants = set()
        for product in getProducts():
            variant_id = product['variant_id']
            if variant_id in seen_variants:
                continue
            seen_variants.add(variant_id)
            writer.writerow([product['handle'], product['sku'],
                            product['title'], product['product_type'],
                            product['vendor'], product['body'],
                            product['tags'],
                            product['option_value'],
                            product['grams'],
                            product['stock'], 
                            product['price'],
                            product['compare_at_price'],
                            product['requires_shipping'],
                            product['taxable'],
                            product['image_src'],
                            product['position']])


if __name__ == '__main__':
    extractProducts(url, 'ambienthomeus-product-page5.csv')

from ast import And
import csv
from http.client import OK
from pickle import EMPTY_DICT
import sys
from unicodedata import category
from xmlrpc.client import ProtocolError
import pandas as pd
import requests
import extruct
from w3lib.html import get_base_url
import urllib.request
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import advertools as adv
data =[]
def checkUrl(url, page):
    fullUrl =url+'?p='+str(page)
    req = requests.get(fullUrl)
    if req.status_code == 200:
        return True
    else:
        return False

def extract_metadata(url):
    r = requests.get(url)
    base_url = get_base_url(r.text, r.url)
    metadata = extruct.extract(r.text, 
                               base_url=base_url,
                               uniform=True,
                               syntaxes=['json-ld',
                                         'microdata',
                                         'opengraph'])
    return metadata

def getProduct(fullUrl):
    metadata= extract_metadata(fullUrl)
    dictionary= metadata
    for key in dictionary:
        if len(dictionary[key]) > 0:
            for item in dictionary[key]:
                if (item['@type'] == 'Product') and (item.get('aggregateRating') is None):
                    #print("Data:", item)
                    title=item['name']
                    imageData = item['image']
                    descriptionData = item['description']
                    sku=item['sku']
                    brand=item['brand']  
                    price=item['offers']['price']
                    availability= item['offers']['availability']
                    category = item['offers']['category']    
                    productDatas = {
                        'Title': title.strip(),
                        'Body(Description)': descriptionData.strip(),
                        'Product Type': category,
                        'Tags': brand,
                        'Image Src': imageData.strip(),
                        'Price': price,
                        'SKU': sku,
                        'Taxable': True,
                        'Requires Shipping': True,
                        'Available': availability
                        }
                    data.append(productDatas)  
    return data
        
def getUrl(url, pNo):  
    initialUrl =url+'?p='+str(pNo)  
    fullUrl =initialUrl
    while checkUrl(url, pNo):
        pNo+=1
        print("Page Number: ", pNo)
        fullUrl=url+'?p='+str(pNo)
        result =getProduct(fullUrl=fullUrl)
        with open('appliancesconnection-faucets-product.csv', 'w', encoding='utf8', newline='') as f:
            writer =csv.DictWriter(f, fieldnames=result[0].keys())
            writer.writeheader()
            writer.writerows(result)
            print("Data Successfully Saved in CSV format")
        
if __name__ == '__main__':
    url = 'https://www.appliancesconnection.com/faucets.html'
    try:
        getUrl(url=url, pNo=1)
        print('started')
    except ProtocolError or ConnectionError:
        print('ended')
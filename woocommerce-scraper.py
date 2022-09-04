
from requests_html import HTMLSession
import csv
url = 'https://www.bbqguys.com/'
s = HTMLSession()
def getLinks(url):
    r =s.get(url)
    items = r.html.find('div.product-small.box')
    links =[]
    for item in items:
        links.append(item.find('a',first=True).attrs['href'])
    
    return links 

def getProduct(link):
    r =s.get(link)
    login_email = r.html.find('input.inputtext _55r1 _6luy').attr('email')
    title = r.html.find('h1', first=True).full_text
    price = r.html.find('span.woocommerce-Price-amount.amount bdi')[1].full_text
    description = r.html.find('div#tab-description', first=True).full_text
    image_src=r.html.find('img.wp-post-image.skip-lazy', first=True).attrs['src']
    
    product ={
        'Title': title.strip(),
        'Price': price.strip(),
        'Description': description.strip(),
        'Image Src': image_src.strip()
    }
    print(product)
    return product

links =getLinks(url)

results=[]
for link in links:
    results.append(getProduct(link))

with open('test.csv', 'w', encoding='utf8', newline='') as f:
    writer =csv.DictWriter(f, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)
    
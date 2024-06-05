import requests
import requests_cache # need this to avoid hours of re-requesting
requests_cache.install_cache()
import csv

import time # need this to insert some waiting time to avoid over-requesting the api
from IPython.core.display import clear_output

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Accept-Version': '3.0',
    "Accept" : "application/hal+json",
    'Content-Type': "application/hal+json"
    
}


url_api = 'https://api.reverb.com/api/listings?product_type=electric-guitars&condition=used'



def iterate_prices(writer):
    for min_price in range(0, 10001, 10):
        if(min_price == 10000):
            max_price = 10000000
        else:
            max_price = min_price + 10

        extract_data('electric-guitars',min_price, max_price, writer)




def extract_data(product_type,price_min, price_max, writer):
    
    page = 1
    numPages = 99999
    items_per_page = 50
    
    while page <= numPages:
        url_api = 'https://api.reverb.com/api/listings?page={}&per_page={}&product_type={}&condition=used&price_min={}&price_max={}'.format(page,items_per_page,product_type, price_min, price_max)
        response = requests.get(url_api, headers=headers)
        if response.status_code != 200:
            print(response.text)
            break

        data = response.json()
        numPages = data['total_pages']
        listing = data["listings"]

        for itemListing in listing:
            print(itemListing['title'])
            print(itemListing['price']['amount'])
            print(itemListing['_links']['web']['href'])
            item = {
                'category' : 'guitarras',
                'image' : itemListing['_links']['photo']['href'],
                'link' : itemListing['_links']['web']['href'],
                'name' : itemListing['title'],
                'price' : itemListing['price']['amount'],
                #'currency' : itemListing['price']['currency'],
                'publish' : itemListing['published_at'], 
                'website' : 'reverb'
            }
            writer.writerow(item)

        if not getattr(response, 'from_cache', False):
            time.sleep(0.35)

        page += 1

with open('reverb.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['category', 'image', 'link', 'name', 'price', 'publish', "website"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    iterate_prices(writer)
from db import SessionLocal, init_db
from models import Product, Offer
import httpx
from rich import print
from rich.logging import RichHandler
import logging
import csv
from extruct.jsonld import JsonLdExtractor
from sqlalchemy.exc import IntegrityError

FORMAT = '%(message)s'
logging.basicConfig(
    level='INFO', format=FORMAT, datefmt='[%X]', handlers=[RichHandler()]
)

def get_urls():
    with open('urls.csv', 'r') as f:
        reader = csv.reader(f)
        urls = [url[0] for url in reader]
    return urls

def get_html(url: str):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
    }
    response = httpx.get(url, headers=headers)
    if response.status_code != 200:
        logging.info(f'url {url} responded with non-200 status code {response.status_code}')
    else:
        extractor = JsonLdExtractor()
        data = extractor.extract(response.text)
        return data

def load_product(session, data):
    product = Product(
        name=data['name'],
        url=data.get('url'),
        description=clean_data(data.get('description')),
        sku=data.get('sku'),
        brand=data['brand']['name']
    )
    try:
        session.add(product)
        session.commit()
    except IntegrityError as error:
        logging.error('f{error}')
        session.rollback()

def load_offers(session, data):
    product = session.query(Product).filter(Product.sku == data['sku']).first()
    if isinstance(data['offers'], list):
        for offer in data['offers']:
            if offer['sku'] == product.sku:
                new_offer = Offer(
                    price=offer['price'],
                    availability=offer.get('availability'),
                    product_id=product.id
                )
    else:
        new_offer = Offer(
            price=data['offers']['price'],
            availability=data['offers'].get('availability'),
            product_id=product.id
        )

    try:
        session.add(new_offer)
        session.commit()
    except IntegrityError as error:
        logging.error('f{error}')
        session.rollback()

def clean_data(value: str|None):
    if value is None:
        return None
    chars_to_remove = ['\n', '\t']
    for char in chars_to_remove:
        value = value.replace(char, '')
    return value.strip()

def main():
    init_db()
    session = SessionLocal()
    urls = get_urls()
    for url in urls:
        product_data = get_html(url)
        for data in product_data:
            if 'offers' in data:
                load_product(session, data)
                load_offers(session, data)

if __name__ == "__main__":
    main()
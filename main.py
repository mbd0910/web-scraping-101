import csv
import json
import time
from dataclasses import asdict, dataclass, fields
from urllib.parse import urljoin

import httpx
from selectolax.parser import HTMLParser


@dataclass
class Product:
    name: str | None
    price: str | None
    metal_points: float | None

def get_html(url: str, **kwargs):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
    }

    if kwargs.get("page"):
        url += str(kwargs.get("page"))
    response = httpx.get(url, headers=headers, follow_redirects=True)
    try:
        response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        print(f'Error response {exc.response.status_code} while requesting {exc.request.url!r}')
        return False
    html = HTMLParser(response.text)
    return html

def extract_text(html, selector):
    try:
        text = html.css_first(selector).text()
        return clean_data(text)
    except AttributeError:
        return None

def remove_new_lines(str: str):
    return str.replace('\n', '').strip()

def parse_page(html):
    products = html.css('div.product-item')

    for product in products:
        yield urljoin("https://www.metalshop.uk/", product.css_first('a').attributes['href'])

def parse_product_page(html):
    product = Product(
        name=extract_text(html, 'div.products_header h1.first'),
        price=extract_text(html, 'div.price span'),
        metal_points=extract_text(html, 'span#detail-credits-amount')
    )
    return asdict(product)

def export_to_json(products):
    with open('products.json', 'w', encoding='utf-8') as f:
        json.dump(products, f, ensure_ascii=False, indent=4)
    print('Saved to JSON')

def export_to_csv(products):
    field_names = [field.name for field in fields(Product)]
    with open('products.csv', 'w') as f:
        writer = csv.DictWriter(f, field_names)
        writer.writeheader()
        writer.writerows(products)
    print('Saved to CSV')

def append_to_csv(products):
    field_names = [field.name for field in fields(Product)]
    with open('append_csv', 'a') as f:
        writer = csv.DictWriter(f, field_names)
        writer.writerows(products)
    print('Appended to CSV')

def clean_data(value: str):
    chars_to_remove = ['\n', '\t']
    for char in chars_to_remove:
        value = value.replace(char, '')
    return value.strip()

def main():
    base_url = "https://www.metalshop.uk/statues-figures/t/discount/pg/"
    products = []
    for page in range(1, 2):
        print(f'Gathering page {page}')
        html = get_html(base_url, page=page)
        if html is False:
            break
        product_urls = parse_page(html)

        for product_url in product_urls:
            print(product_url)
            html = get_html(product_url)
            products.append(parse_product_page(html))
            time.sleep(1)

    export_to_json(products)
    export_to_csv(products)



if __name__ == '__main__':
    main()

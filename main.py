import httpx
from selectolax.parser import HTMLParser
import time

def get_html(base_url: str, page: int):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
    }

    url = base_url + str(page)
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
        return html.css_first(selector).text()
    except AttributeError:
        return None

def remove_new_lines(str: str):
    return str.replace('\n', '').strip()

def parse_page(html):
    products = html.css('div.product-item')

    for product in products:
        product_name = extract_text(product, 'div.product-item-name h2')
        product_price = remove_new_lines(extract_text(product, 'div.products_price'))

        item = {
            'name': product_name,
            'price': product_price
        }

        yield item

def main():
    base_url = "https://www.metalshop.uk/statues-figures/t/discount/pg/"
    for page in range(1, 6):
        print(f'Gathering page {page}')
        html = get_html(base_url, page)
        if html is False:
            break
        data = parse_page(html)

        for item in data:
            print(item)

        time.sleep(1)


if __name__ == '__main__':
    main()

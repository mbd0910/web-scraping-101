import httpx
from selectolax.parser import HTMLParser

def get_html(base_url: str, page: int):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
    }

    url = base_url + str(page)
    response = httpx.get(url, headers=headers, follow_redirects=True)
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
    items = []

    for product in products:
        product_name = extract_text(product, 'div.product-item-name h2')
        product_price = remove_new_lines(extract_text(product, 'div.products_price'))

        item = {
            'name': product_name,
            'price': product_price
        }

        items.append(item)

    return items

def main():
    base_url = "https://www.metalshop.uk/statues-figures/t/discount/pg/"
    for i in range(1, 6):
        items = parse_page(get_html(base_url, i))
        print(items)
        print(len(items))

if __name__ == '__main__':
    main()

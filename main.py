import httpx
from selectolax.parser import HTMLParser

def get_html(base_url: str):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
    }

    response = httpx.get(base_url, headers=headers)
    html = HTMLParser(response.text)
    return html

def extract_text(html, selector):
    try:
        return html.css_first(selector).text()
    except AttributeError:
        return None

def remove_new_lines(str: str):
    return str.replace('\n', '')

def parse_page(html):
    products = html.css('div.grid-tile')
    items = []

    for product in products:
        product_name_spans = product.css('div.product-name span')
        parts = []
        for span in product_name_spans:
            if span.attributes['class'] == 'spacer':
                parts.append(' / ')
            else:
                parts.append(remove_new_lines(span.text()))
        product_name = str.join(' ', parts)
        product_price = extract_text(product, 'span.currentprice')
        if product_price is not None:
            product_price = remove_new_lines(product_price)

        item = {
            'name': product_name,
            'price': product_price
        }

        items.append(item)

    return items

def main():
    base_url = "https://www.emp.co.uk/band-merch/t-shirts/"
    items = parse_page(get_html(base_url))
    print(items)

if __name__ == '__main__':
    main()

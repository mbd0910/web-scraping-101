import httpx
from selectolax.parser import HTMLParser

url = "https://www.emp.co.uk/band-merch/t-shirts/"

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
}

response = httpx.get(url, headers=headers)
html = HTMLParser(response.text)

def extract_text(html, selector):
    try:
        return html.css_first(selector).text()
    except AttributeError:
        return None

products = html.css('div.grid-tile')

for product in products:
    product_name_spans = product.css('div.product-name span')
    parts = []
    for span in product_name_spans:
        if span.attributes['class'] == 'spacer':
            parts.append(' / ')
        else:
            parts.append(span.text().removeprefix('\n').removesuffix('\n'))
    product_name = str.join(' ', parts)
    product_price = extract_text(product, 'span.currentprice')

    item = {
        'name': product_name,
        'price': product_price
    }

    print(item)


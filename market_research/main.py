from curl_cffi import requests
from selectolax.parser import HTMLParser
import json
from rich import print
import re

def remove_trailing_commas(json_str):
    # Regular expression to find and remove trailing commas
    json_str = re.sub(r',\s*([}\]])', r'\1', json_str)
    return json_str

url = 'https://ravecoffee.co.uk/products/best-selling-coffee-bundle?variant=19949439418422'
response = requests.get(url, impersonate='chrome120')
html = HTMLParser(response.text)
scripts = html.css("script[type='application/ld+json']")

for script in scripts:
    if 'offers' in script.text():
        data = json.loads(remove_trailing_commas(script.text()))
        print(data.get('offers'))


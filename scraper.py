import scraperwiki
import json
import re
import urlparse
import lxml.html

def scrape_laptop(url):
    html = scraperwiki.scrape(url)
    tree = lxml.html.fromstring(html)
    title = tree.find('.//h1')
    price = tree.find('.//span[@id="fk-mprod-our-id"]')
    data = {
        'title': title.text if title is not None else '',
        'url': url,
        'price': price.text_content() if price is not None else ''
    }
    for row in tree.findall('.//table[@class="fk-specs-type2"]//tr'):
        label = row.find('th')
        value = row.find('td')
        if label is not None and value is not None and label.text is not None:
            # Ensure key is simple text. 
            key = re.sub(r'[^a-zA-Z0-9_\- ]+', '-', label.text)
            data[key] = value.text
    scraperwiki.sqlite.save(unique_keys=["url"], data=data)

start = 0
while True:
    data = scraperwiki.scrape('http://www.flipkart.com/computers/laptops/all?response-type=json&inf-start=%d' % start)
    print data;

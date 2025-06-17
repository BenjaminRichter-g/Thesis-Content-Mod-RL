#!/usr/bin/env python3
from bs4 import BeautifulSoup

# load your HTML (either from a file or a string)
with open('blocked_domains.html', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

hate_domains = []
for block in soup.select('.about__domain-blocks__domain'):
    reason_el = block.find('p')
    if reason_el and reason_el.get_text(strip=True) == 'Hate speech':
        # the domain lives inside the <h6><span> text
        domain_span = block.select_one('h6 > span')
        if domain_span:
            hate_domains.append(domain_span.get_text(strip=True))

# output
for d in hate_domains:
    print(d)


with open('hate_domains.txt', 'w', encoding='utf-8') as f:
    for domain in hate_domains:
        f.write(domain + '\n')

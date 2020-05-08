from bs4 import BeautifulSoup
import os
import json
import sys

from utils import get_p_html

base_url= 'https://www.lesraffineurs.com/'

def main(max_prods = 10e9):

    prods = []
    pages = range(1,9)
    
    prod_count = 0

    for page in pages:

        print('page: {}'.format(page))
        url = '22-tous-les-produits?page={}'.format(page)
        url = os.path.join(base_url, url)
        htmlBytes, _ = get_p_html(url)
        soup = BeautifulSoup(htmlBytes, 'html.parser')
        soup_products = soup.findAll(attrs={'class': 'thumbnail-container'})

        for prod in soup_products:

            info = prod.findAll('a')

            prod = {}
            prod['href'], prod['name'] = info[1].get("href"), info[1].text
            prod['image'] = info[0].findAll('source')[0].get('data-srcset')
            prod['id'] = prod['href'].split('/')[-1].split('-')[0]
            prods.append(prod)
            print('\t{}'.format(prod['name']))

            prod_count += 1

            if prod_count >  max_prods:
                break

        if prod_count >  max_prods:
                break
        print('\n')

    with open('prods.json', 'w') as fp:
        json.dump(prods, fp)
        
if __name__ == '__main__':
    if len(sys.argv) >= 2:
        main(max_prods = int(sys.argv[1]))
    else:
        main()
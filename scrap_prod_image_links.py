from bs4 import BeautifulSoup
import os
import json
import sys

from utils import get_p_html

def get_images_from_soup(soup):
    image_soup = soup.findAll(attrs={'class': 'product-image'})
    images = []
    
    for img in image_soup:
        
        # case 1
        url = img.findAll('img')[0].get('data-src')
        if url:
            images.append(url)
            
        # case 2
        url = img.findAll('img')[0].get('src')
        if url and 'https' in url:
            images.append(url)
            
    return images

def main(max_prods = 10e9):

    with open('prods.json', 'r') as fp:
        prods = json.load(fp)
    
    count_prods = 0
    for prod in prods:
        print(prod['name'])
        count_prods +=1

        # fetch HTML code
        url = prod['href']
        htmlBytes, _ = get_p_html(url)
        soup = BeautifulSoup(htmlBytes, 'html.parser')

        # extract image links
        prod['images'] = get_images_from_soup(soup)

        # a bit of cleaning
        prod['thumb_img'] = prod.pop('image')
        prod['category'] = url.split('/')[-2]

        if count_prods >= max_prods:
            break

    with open('prods_w_images.json', 'w') as fp:
        json.dump(prods, fp)
        
if __name__ == '__main__':
    if len(sys.argv) >= 2:
        main(max_prods = int(sys.argv[1]))
    else:
        main()
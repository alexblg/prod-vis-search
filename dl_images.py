from bs4 import BeautifulSoup
import os
import json
import sys

from utils import save_img

save_dir = r'/home/alex/data/wir/'
source_dir = r'raffineurs'
save_dir = os.path.join(save_dir, source_dir)
base_url= 'https://www.lesraffineurs.com/'

def main(max_prods = 10e9):
    prod_count = 0
    
    with open('prods_w_images.json', 'r') as fp:
        prods = json.load(fp)

    for prod in prods:
        print(prod['name'])
        prod_count += 1
        
        for img_url in prod['images']:
            url = img_url
            img_name = '-'.join([prod['id']]+url.split('/')[-2:])
            print('\t'+img_name)
            image_local_path = os.path.join(
                save_dir
                ,img_name)
            save_img(url, image_local_path)

        if prod_count >  max_prods:
                break
        
if __name__ == '__main__':
    if len(sys.argv) >= 2:
        main(max_prods = int(sys.argv[1]))
    else:
        main()
from urllib.request import urlopen, Request  
from bs4 import BeautifulSoup
import os
import json
import re

def get_p_html(url):
    req = Request(
        url, 
        data=None, 
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/82.0.4074.0 Safari/537.36'
        }
    )
    f = urlopen(req)
    try:
        return f.read().decode('utf-8'), f.geturl()
    except:
        return f.read(), f.geturl()
    
from urllib.error import HTTPError
from urllib.request import urlretrieve

def save_img(image_url, image_local_path):
    try:
        urlretrieve(image_url, image_local_path)
    except FileNotFoundError as err:
        print(err)   # something wrong with local path
    except HTTPError as err:
        print(err)  # something wrong with url
        
def download_images(page_img_links):
    for img in page_img_links:
        url = os.path.join(base_url, img['href'][1:])
        image_local_path = os.path.join(
            save_dir
            ,source_dir+'_'+img.split('/')[-1])
        save_img(url, image_local_path)
        print('saved {} at {}'.format(url, image_local_path))
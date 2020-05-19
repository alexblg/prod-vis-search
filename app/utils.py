# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""
import os
import pandas as pd

def get_prod_name_from_img_name(img_list, path='static/prod_inventory.csv'):
    df = pd.read_csv(path)
    return [
        df.query("id == '{}'".format(img.split('-')[0])).name.values[0]
        for img in img_list]

from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords

tokenizer = RegexpTokenizer(r'\w+')
stop_words = set(stopwords.words('english'))

def parse_query(q):
    # tokenize (lower, and retain alphanum only)
    parsed_q = tokenizer.tokenize(q.lower())

    # remove stopwords
    parsed_q = [w for w in parsed_q if not w in stop_words]
    
    return parsed_q
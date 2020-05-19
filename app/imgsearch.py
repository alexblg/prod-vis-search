# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""
import os
import pandas as pd
import random
import numpy as np

get_img_name_from_href = lambda prod_id, href: '-'.join([prod_id]+href.split('/')[-2:])
get_img_name = lambda sel_id, img_id: get_img_name_from_href(df.loc[sel_id, 'id'], df.loc[sel_id, 'images'][img_id])

IMG_PATH = r"C:\Users\alexa\Documents\data\wir\project\raffineurs"
IMG_INVENTORY_PATH = 'static/img_inventory.csv'
IMG_STATIC_LIST = ['1015-8599-large_default-votre-portrait-dans-un-studio-du-xixeme-siecle.jpg',
 '1033-8975-large_default-mug-egoist-feminisit-anarchist-pessimist-optimist.jpg',
 '1058-14147-large_default-t-shirt-smoking-pipe.jpg',
 '1087-9246-large_default-cube-en-bois-magnetique.jpg',
 '1128-13515-large_default-rendez-vous-pour-creer-votre-creme-sur-mesure.jpg',
 '1160-9831-large_default-un-terrarium-a-composer-soi-meme.jpg',
 '1191-10092-large_default-maillot-de-bain-iguazu.jpg',
 '1215-10321-large_default-affiche-50-choses-a-faire-dans-une-vie.jpg',
 '1244-10653-large_default-carnet-de-projets.jpg',
 '1261-10675-large_default-affiches-ville-mondrian.jpg']

image_search_res0 = lambda x: IMG_STATIC_LIST

def image_search_res1(query, path=IMG_INVENTORY_PATH):
    df = pd.read_csv(path)
    idxs = [random.randrange(df.shape[0]) for i in range(10)]
    return df.iloc[idxs].image_name.tolist()

from sklearn.feature_extraction.text import CountVectorizer

def image_search_res2(query, path='static/img_top10_labels.csv'):
    # load image label data
    df = pd.read_csv(path)

    # generate BoW
    vect = CountVectorizer()
    bow = vect.fit_transform(df.content.tolist())
    voc = vect.vocabulary_
    
    if query in voc:
        img_idx = list(np.where(bow[:,voc[query]].todense() >0)[0])
        return df.loc[img_idx, 'image_name'].tolist()
    else:
        return []

from numpy.linalg import norm

def cosine_sim(a, b):
    return np.dot(a, b.T) / (norm(a)*norm(b.T))

def image_search_res3(query, path='static/img_top10_labels.csv'):
    # load image label data
    df = pd.read_csv(path)

    # generate BoW
    vect = CountVectorizer()
    bow = vect.fit_transform(df.content.tolist())
    voc = vect.vocabulary_
    
    # get query representation
    q = vect.transform([query]).todense()
    
    # rank results
    ranks = cosine_sim(q, bow.todense()[:,:])
    ranks = np.asarray(ranks)[0]
    ranked_idx = np.argsort(-ranks)
    
    return df.loc[ranked_idx,'image_name'].tolist()[:12]
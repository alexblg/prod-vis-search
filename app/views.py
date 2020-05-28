# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

# Python modules
import os 

# Flask modules
from flask               import render_template, request, url_for, redirect, send_from_directory

# App modules
from app        import app, model, img_emb_dict
from app.forms  import ProdSearch

# search models
from .imgsearch import image_search_res5
from .utils import get_prod_name_from_img_name

# Product search
@app.route('/search', methods=['GET', 'POST'])
def search():
    
    # Declare the form
    form = ProdSearch(request.form)

    # Flask message injected into the page, in case of any errors
    msg = None

    if request.method == 'GET':
        return render_template( 'pages/search.html', form=form, msg=msg )

    # check if both http method is POST and form is valid on submit
    if form.validate_on_submit():

        # assign form data to variables
        query = request.form.get('query', '', type=str)
        print('query: '+str(query))

    else:
        msg = 'Input error: text should be shorter than 64 characters'

    # get query image results
    img_list = image_search_res5(query, img_emb_dict, model, labelled_df_path='app/static/img_top10_labels_w_weights.csv', thresh=0.2)
    #import pickle
    #with open(r"app/static/image_list.pkl", "rb") as f:
    #    img_list = pickle.load(f)
    img_list = [img[0] for img in img_list]
    prod_names = get_prod_name_from_img_name(img_list, path='app/static/prod_inventory.csv') # corresponding product names

    # select top 12 results (later replace by pagination)
    img_list = img_list[:12]

    return render_template( 'pages/results.html', len=len(img_list), res=img_list, img_info=prod_names, msg=msg )


# Product search
@app.route('/results')
def results():
    
    # Flask message injected into the page, in case of any errors
    msg = None

    return render_template('pages/results.html', msg=msg)

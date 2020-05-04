# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

# Python modules
import os, logging 

# Flask modules
from flask               import render_template, request, url_for, redirect, send_from_directory
from werkzeug.exceptions import HTTPException, NotFound, abort

# App modules
from app        import app
from app.forms  import ProdSearch

# Product search
@app.route('/search.html', methods=['GET', 'POST'])
def search():
    
    # Declare the form
    form = ProdSearch(request.form)

    # Flask message injected into the page, in case of any errors
    msg = None

    # check if both http method is POST and form is valid on submit
    if form.validate_on_submit():

        # assign form data to variables
        query = request.form.get('query', '', type=str)

    return render_template('pages/search.html', form=form, msg=msg )

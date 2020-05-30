# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

import os

from flask            import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt     import Bcrypt

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config.from_object('app.configuration.Config')

db = SQLAlchemy  (app) # flask-sqlalchemy
bc = Bcrypt      (app) # flask-bcrypt

temp_var = 32

import pickle
import fasttext

global model, img_emb_dict
model, img_emb_dict = None, None
if True:
	print('loading embedding model..')
	data_path = r"C:\Users\alexa\Documents\data\wir\project"
	fname = r"cc.en.300.bin"
	model = fasttext.load_model(
		os.path.join(data_path, fname))

	print('loading image embeddings..')	
	with open(r"app/static/img_emb_dict.pkl", "rb") as f:
	    img_emb_dict = pickle.load(f)

# Setup database
@app.before_first_request
def initialize_database():
    db.create_all()

# Import routing, models and Start the App
from app import views, models

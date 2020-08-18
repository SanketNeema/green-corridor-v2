from flask import Flask 
import os
import firebase_admin
from firebase_admin import credentials, firestore
from flask_bcrypt import Bcrypt

#from flask_login import LoginManager

app = Flask(__name__)
#app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

cred = credentials.Certificate('serviceAccountKeySIHProject.json')
firebase_admin.initialize_app(cred)
db = firestore.client() 
#bcrypt = Bcrypt(app)
#login_manager = LoginManager(app)

from green_corridor import routes
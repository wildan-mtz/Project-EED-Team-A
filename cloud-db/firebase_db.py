import firebase_admin
from firebase_admin import db
import datetime

cred_obj = firebase_admin.credentials.Certificate('service-account-privatekey.json')
default_app = firebase_admin.initialize_app(cred_obj, {
    	'databaseURL':'https://database-eed-default-rtdb.asia-southeast1.firebasedatabase.app'
    	})
from firebase_admin import db
ref = db.reference("/")
import json
with open("testing.json", "r") as f:
	file_contents = json.load(f)
ref.set(file_contents)
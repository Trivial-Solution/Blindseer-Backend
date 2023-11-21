from datetime import datetime

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import time

def generate_unique_id():
    timestamp = time.time()
    dt_object = datetime.fromtimestamp(timestamp)
    unique_id = dt_object.strftime("%Y-%m-%d-%H:%M:%S")
    return unique_id

unique_id = generate_unique_id()
print(unique_id)

cred = credentials.Certificate('blindseer-cfefc-firebase-adminsdk-h2tky-ac28da08b2.json')
firebase_admin.initialize_app(cred)

db = firestore.client()


doc_ref = db.collection('texts').document(unique_id)
doc_ref.set({
    'descr': 'This is a sample text'
})
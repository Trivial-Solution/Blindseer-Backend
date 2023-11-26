from datetime import datetime

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import time


class FirestoreManager():
    def __init__(self):
        self.cred = credentials.Certificate('keys/blindseer-cfefc-firebase-adminsdk-h2tky-ac28da08b2.json')
        firebase_admin.initialize_app(self.cred)

    def upload_text(self, text: str):
        db = firestore.client()
        doc_ref = db.collection('texts').document(FirestoreManager.__generate_unique_id())
        doc_ref.set({
            'descr': text
        })

    @staticmethod
    def __generate_unique_id():
        timestamp = time.time()
        dt_object = datetime.fromtimestamp(timestamp)
        unique_id = dt_object.strftime("%Y-%m-%d-%H-%M-%S")
        return unique_id

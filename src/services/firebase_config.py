import firebase_admin
from firebase_admin import credentials, firestore, auth

# Ruta al archivo JSON de credenciales de Firebase
CRED_PATH = 'ciltivo-safedata-firebase-adminsdk-5a91k-14126ad6c4.json'

# Variable para almacenar la instancia de la aplicación Firebase
firebase_app = None

def initialize_firebase():
    global firebase_app
    if not firebase_admin._apps:
        cred = credentials.Certificate(CRED_PATH)
        firebase_app = firebase_admin.initialize_app(cred)
    return firebase_app

def get_firestore_db():
    if not firebase_admin._apps:
        initialize_firebase()
    return firestore.client()

def get_firebase_auth():
    if not firebase_admin._apps:
        initialize_firebase()
    return auth


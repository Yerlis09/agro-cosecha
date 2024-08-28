import os

class Config:
    # Configuración de la clave secreta
    SECRET_KEY = os.urandom(24).hex()
    WTF_CSRF_SECRET_KEY = SECRET_KEY
    
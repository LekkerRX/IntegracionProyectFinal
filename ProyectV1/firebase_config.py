import firebase_admin
from firebase_admin import credentials

# Ruta correcta al archivo JSON de credenciales
cred = credentials.Certificate("ProyectV1/chat-98e8c-firebase-adminsdk-2sjfp-4d69c8e2f8.json")

# Inicializa Firebase con las credenciales
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://chat-98e8c-default-rtdb.firebaseio.com'
})

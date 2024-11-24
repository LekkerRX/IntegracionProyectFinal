import firebase_admin
from firebase_admin import credentials, db

# Inicializa la conexión con Firebase usando la clave de servicio
cred = credentials.Certificate('ProyectV1/chat-98e8c-firebase-adminsdk-2sjfp-4d69c8e2f8.json')  # Ruta al archivo JSON
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://chat-98e8c-default-rtdb.firebaseio.com'  # Reemplaza con tu URL de Realtime Database
})

# Crear una nueva entrada de chat
def crear_chat(cliente_id, tecnico_id, publicacion_id):
    # Referencia a la ubicación "chats" en la base de datos
    ref = db.reference('chats')
    
    # Crear un nuevo chat
    nuevo_chat = ref.push({
        'cliente': cliente_id,
        'tecnico': tecnico_id,
        'publicacion': publicacion_id
    })

    # Obtener el ID del nuevo chat
    chat_id = nuevo_chat.key
    print(f"Nuevo chat creado con ID: {chat_id}")
    return chat_id

# Crear un nuevo mensaje dentro de un chat
def crear_mensaje(chat_id, remitente_id, contenido, fecha):
    # Referencia al chat específico
    ref = db.reference(f'chats/{chat_id}/mensajes')
    
    # Crear un nuevo mensaje
    mensaje_ref = ref.push({
        'contenido': contenido,
        'remitente': remitente_id,
        'fecha': fecha  # Fecha en formato timestamp
    })

    print(f"Nuevo mensaje enviado con ID: {mensaje_ref.key}")

# Ejemplo de uso
if __name__ == '__main__':
    # Datos del chat
    cliente_id = 'usuario_id_cliente'
    tecnico_id = 'usuario_id_tecnico'
    publicacion_id = 'id_publicacion'

    # Crear un chat
    chat_id = crear_chat(cliente_id, tecnico_id, publicacion_id)

    # Crear un mensaje dentro del chat
    crear_mensaje(chat_id, cliente_id, 'Hola, ¿cómo puedo ayudarte?', 1234567890)
    crear_mensaje(chat_id, tecnico_id, '¡Hola! ¿En qué necesitas ayuda?', 1234567900)

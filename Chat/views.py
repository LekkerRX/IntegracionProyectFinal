from django.shortcuts import render



from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Chat, Mensaje
from django.contrib.auth.decorators import login_required


from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import firebase_admin
from firebase_admin import db

# Asegúrate de que Firebase esté inicializado
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import firebase_admin
from firebase_admin import db
from datetime import datetime

if not firebase_admin._apps:
    cred = firebase_admin.credentials.Certificate("ProyectV1/chat-98e8c-firebase-adminsdk-2sjfp-4d69c8e2f8.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://chat-98e8c-default-rtdb.firebaseio.com'
    })
else:
    print("Firebase ya está inicializado.")

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import firebase_admin
from firebase_admin import db
from datetime import datetime
from User.models import User



# views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from datetime import datetime
from firebase_admin import db

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from firebase_admin import db
from datetime import datetime
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from datetime import datetime
from django.contrib.auth.models import User
from firebase_admin import db

@login_required
def detalle_chat(request, chat_id):
    # Referencia al chat en Firebase
    chat_ref = db.reference(f"chats/{chat_id}")

    # Verificar si el chat existe y si el usuario tiene acceso
    chat_data = chat_ref.get()
    if chat_data:
        cliente_id = chat_data.get('cliente')
        tecnico_id = chat_data.get('tecnico')

        # Verificar que el usuario esté relacionado con el chat
        if str(request.user.id) != cliente_id and str(request.user.id) != tecnico_id:
            return JsonResponse({"error": "Acceso no autorizado."}, status=403)
    else:
        return JsonResponse({"error": "Chat no encontrado."}, status=404)

    # Obtener los mensajes desde Firebase, ordenados por fecha
    mensajes_ref = chat_ref.child("mensajes")
    mensajes = mensajes_ref.order_by_child('fecha').get() or {}

    # Manejar el envío de un mensaje
    if request.method == 'POST':
        contenido = request.POST.get('contenido')
        if contenido:
            mensaje_data = {
                'contenido': contenido,
                'remitente': str(request.user.id),
                'remitente_nombre': request.user.username,
                'fecha': datetime.now().isoformat()  # Usar la fecha actual en formato ISO
            }
            # Agregar el mensaje a Firebase
            mensajes_ref.push(mensaje_data)

            # Obtener nuevamente los mensajes después de agregar el nuevo
            mensajes = mensajes_ref.order_by_child('fecha').get() or {}

    # Obtener los nombres de cliente y técnico
    try:
        cliente = User.objects.get(id=cliente_id)
    except User.DoesNotExist:
        cliente = None

    try:
        tecnico = User.objects.get(id=tecnico_id)
    except User.DoesNotExist:
        tecnico = None

    # Crear una lista de mensajes con los nombres de los remitentes
    mensajes_con_nombres = []
    for mensaje in mensajes.values():
        usuario_id = mensaje['remitente']
        try:
            usuario = User.objects.get(id=usuario_id)
            mensaje['remitente_nombre'] = usuario.username
        except User.DoesNotExist:
            mensaje['remitente_nombre'] = 'Usuario desconocido'
        mensajes_con_nombres.append(mensaje)

    # Renderizar la página del chat con los mensajes actuales
    return render(request, 'detalle_chat.html', {
        'chat': chat_data,
        'mensajes': mensajes_con_nombres,
        'chat_id': chat_id,  # Pasamos el chat.id al contexto
        'cliente_nombre': cliente.username if cliente else 'Cliente desconocido',
        'tecnico_nombre': tecnico.username if tecnico else 'Técnico desconocido'
    })







from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import firebase_admin
from firebase_admin import db



from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from datetime import datetime
from django.contrib.auth.models import User
from firebase_admin import db

@login_required
def detalle_chat_tecnico(request, chat_id):
    # Referencia al chat en Firebase
    chat_ref = db.reference(f"chats/{chat_id}")
    print(f"Chat ID recibido: {chat_id}")  # Verifica el valor del ID recibido

    # Verificar si el chat existe y si el usuario tiene acceso
    chat_data = chat_ref.get()
    if chat_data:
        cliente_id = chat_data.get('cliente')
        tecnico_id = chat_data.get('tecnico')
        
        # Verificar que el usuario esté relacionado con el chat y que sea un técnico
        if str(request.user.id) != tecnico_id:
            return JsonResponse({"error": "Acceso no autorizado."}, status=403)
    else:
        return JsonResponse({"error": "Chat no encontrado."}, status=404)

    # Obtener los mensajes desde Firebase
    mensajes_ref = chat_ref.child("mensajes")
    mensajes = mensajes_ref.order_by_child('fecha').get() or {}

    # Manejar el envío de un mensaje
    if request.method == 'POST':
        contenido = request.POST.get('contenido')
        if contenido:
            mensaje_data = {
                'contenido': contenido,
                'remitente': str(request.user.id),
                'fecha': datetime.now().isoformat()  # Usar la fecha actual en formato ISO
            }
            # Agregar el mensaje a Firebase
            mensajes_ref.push(mensaje_data)

            # Obtener nuevamente los mensajes después de agregar el nuevo
            mensajes = mensajes_ref.order_by_child('fecha').get() or {}

    # Obtener los nombres de cliente y técnico
    try:
        cliente = User.objects.get(id=cliente_id)
    except User.DoesNotExist:
        cliente = None

    try:
        tecnico = User.objects.get(id=tecnico_id)
    except User.DoesNotExist:
        tecnico = None

    # Crear una lista de mensajes con los nombres de los remitentes
    mensajes_con_nombres = []
    for mensaje in mensajes.values():
        usuario_id = mensaje['remitente']
        try:
            usuario = User.objects.get(id=usuario_id)
            mensaje['remitente_nombre'] = usuario.username
        except User.DoesNotExist:
            mensaje['remitente_nombre'] = 'Usuario desconocido'
        mensajes_con_nombres.append(mensaje)

    # Renderizar la página del chat con los mensajes actuales
    return render(request, 'chats_tecnico.html', {
        'chat': chat_data,
        'mensajes': mensajes_con_nombres,
        'chat_id': chat_id,
        'cliente_nombre': cliente.username if cliente else 'Cliente desconocido',
        'tecnico_nombre': tecnico.username if tecnico else 'Técnico desconocido'
    })





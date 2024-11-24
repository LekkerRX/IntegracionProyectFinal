from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import PublicacionForm
from .models import Publicacion, Oficio
from Aceptaciones.models import Aceptacion


@login_required
def eliminar_publicacion(request, publicacion_id):
    # Intentamos obtener la publicación, si no existe se lanza un 404
    publicacion = get_object_or_404(Publicacion, id=publicacion_id, cliente=request.user)
    
    # Eliminar la publicación
    publicacion.delete()
    
    # Mensaje de éxito
    messages.success(request, 'La publicación ha sido eliminada correctamente.')
    
    # Redirigir de nuevo a la página de gestionar publicaciones
    return redirect('Post:gestionar_publicaciones')


from Notificaciones.models import Notification  # Importar el modelo de notificaciones


@login_required
def gestionar_publicaciones(request):
    # Obtener el parámetro de orden de la URL (si existe)
    sort_order = request.GET.get('sort', 'desc')  # Por defecto, ordenar de mayor a menor

    # Filtrar las publicaciones del usuario
    publicaciones = Publicacion.objects.filter(cliente=request.user)

    # Optimizar la carga de los oficios relacionados usando prefetch_related
    publicaciones = publicaciones.prefetch_related('oficios', 'aceptacion_set__tecnico')

    # Ordenar las publicaciones según el parámetro 'sort'
    publicaciones = publicaciones.order_by('fecha_publicacion' if sort_order == 'asc' else '-fecha_publicacion')

    # Actualizar el estado de la publicación según las aceptaciones
    for publicacion in publicaciones:
        if publicacion.aceptacion_set.exists():
            publicacion.estado = 'Postulaciones recibidas'
        else:
            publicacion.estado = 'esperando tecnico'
        publicacion.save()

    # Obtener las notificaciones relacionadas con el usuario autenticado
    notificaciones = Notification.objects.filter(user=request.user).order_by('-created_at')
    
    # Obtener los chats activos del cliente
    chats_activos = Chat.objects.filter(cliente=request.user)

    if request.method == 'POST':
        publicacion_id = request.POST.get('publicacion_id')  # Obtener el ID de la publicación si está presente
        publicacion = None

        if publicacion_id:
            publicacion = get_object_or_404(Publicacion, id=publicacion_id, cliente=request.user)

        form = PublicacionForm(request.POST, request.FILES, instance=publicacion, user=request.user)

        if form.is_valid():
            publicacion = form.save(commit=False)
            publicacion.cliente = request.user
            publicacion.save()
            form.save_m2m()
            messages.success(request, 'Publicación guardada correctamente.')
            return redirect('Post:gestionar_publicaciones')
        else:
            for field in form:
                for error in field.errors:
                    messages.error(request, error)

    else:
        publicacion_id = request.GET.get('publicacion_id')
        publicacion = None

        if publicacion_id:
            publicacion = get_object_or_404(Publicacion, id=publicacion_id, cliente=request.user)

        form = PublicacionForm(instance=publicacion, user=request.user)

    for publicacion in publicaciones:
        if publicacion.aceptacion_set.exists():
            tecnico = publicacion.aceptacion_set.first().tecnico
            publicacion.tecnico_id = tecnico.id

    return render(request, 'gestionar_publicaciones.html', {
        'form': form,
        'publicaciones': publicaciones,
        'notificaciones': notificaciones,
        'chats_activos':chats_activos,
    })



from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404
from Chat.models import Chat
from Post.models import Publicacion  # Asegúrate de importar el modelo Publicacion
from User.models import Tecnico

from firebase_admin import db
from django.contrib import messages
from Notificaciones.models import Notification  # Asegúrate de tener el modelo de notificaciones importado

@login_required
def aceptar_tecnico(request):
    if request.method == 'POST':
        publicacion_id = request.POST.get('publicacion_id')
        tecnico_id = request.POST.get('tecnico_id')

        if not publicacion_id or not tecnico_id:
            raise Http404("Publicación o técnico no especificado.")

        # Obtener la publicación
        publicacion = get_object_or_404(Publicacion, id=publicacion_id, cliente=request.user)

        # Verificar que el técnico haya postulado
        aceptacion = publicacion.aceptacion_set.filter(tecnico_id=tecnico_id).first()
        if not aceptacion:
            messages.error(request, "El técnico seleccionado no ha postulado a esta publicación.")
            return redirect('Post:gestionar_publicaciones')

        # Obtener el técnico y su usuario relacionado
        tecnico = get_object_or_404(Tecnico, id=tecnico_id)
        tecnico_user = tecnico.user  # Relación OneToOne con el modelo User

        # Actualizar el estado de la publicación
        publicacion.estado = 'tecnico atendiendo'
        publicacion.tecnico_id = tecnico_id
        publicacion.save()

        # Crear el chat entre cliente y técnico en Django
        chat = Chat.objects.create(
            tecnico=tecnico_user,  # Usuario relacionado con el técnico
            cliente=publicacion.cliente,  # Usuario cliente
            publicacion=publicacion
        )

        # Crear el chat en Firebase
        chat_ref = db.reference('chats')
        chat_id = chat.id  # Usamos el ID del chat de Django

        chat_ref.child(str(chat_id)).set({
            'cliente': str(publicacion.cliente.id),
            'tecnico': str(tecnico_user.id),
            'publicacion': str(publicacion.id),
            'mensajes': {}  # Inicializar sin mensajes
        })

        # Crear la notificación para el técnico
        mensaje_notificacion = f"Fuiste aceptado para atender la publicación: {publicacion.titulo}."
        notificacion = Notification.objects.create(
            user=tecnico_user,  # Usuario técnico
            message=mensaje_notificacion,
            is_read=False
        )

        # Mostrar un mensaje de éxito al cliente
        messages.success(request, f"Has aceptado al técnico {tecnico.nombre}.")
        return redirect('Post:gestionar_publicaciones')

    raise Http404("Método no permitido.")


from django.shortcuts import get_object_or_404, redirect

from User.models import Tecnico
from Aceptaciones.models import Aceptacion

def eliminar_tecnico(request, publicacion_id, tecnico_id):
    publicacion = get_object_or_404(Publicacion, id=publicacion_id)
    tecnico = get_object_or_404(Tecnico, id=tecnico_id)
    
    # Encuentra la aceptación correspondiente y elimínala
    aceptacion = get_object_or_404(Aceptacion, publicacion=publicacion, tecnico=tecnico)
    aceptacion.delete()

    # Cambiar el campo 'visible_para_tecnicos' a True si no hay más técnicos postulados
    if publicacion.aceptacion_set.count() == 0:
        publicacion.visible_para_tecnicos = True
        publicacion.save()

    # Agregar mensaje de éxito
    messages.success(request, 'Técnico eliminado correctamente.')
    
    # Redirige de nuevo a la página de gestión de publicaciones
    return redirect('Post:gestionar_publicaciones')




from django import template
import json

register = template.Library()

@register.filter
def jsonify(value):
    return json.dumps([oficio.nombre for oficio in value])

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from Notificaciones.models import Notification

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from Notificaciones.models import Notification

@login_required
def eliminar_notificacion_tecnico(request, notificacion_id):
    # Obtener la notificación o 404 si no existe
    notificacion = get_object_or_404(Notification, id=notificacion_id, user=request.user)
    
    # Verificar si el usuario es un técnico
    if not hasattr(request.user, 'tecnico'):
        # Si no es técnico, redirigir o lanzar error
        return redirect('User:publicaciones_tecnico')  # Redirigir a la página de publicaciones del técnico

    # Eliminar la notificación
    notificacion.delete()

    # Redirigir a la página deseada
    return redirect('User:publicaciones_tecnico')  # Cambia el nombre según la vista que corresponda


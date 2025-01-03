from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from Credencial.models import Credencial
from Oficio.models import Oficio
from django.db.models import Q
from django.utils import timezone
from Notificaciones.models import Notification

@login_required
def lista_credenciales(request):
    # Filtrar por tipo de oficio y fecha de subida
    notificaciones = Notification.objects.filter(user=request.user).order_by('-created_at')
    oficio_filter = request.GET.get('oficio')
    fecha_filter = request.GET.get('fecha')
    orden = request.GET.get('orden', 'desc')  # Añadir el parámetro de orden por defecto es descendente

    credenciales = Credencial.objects.all()

    if oficio_filter:
        credenciales = credenciales.filter(oficio__id=oficio_filter)
    
    if fecha_filter:
        try:
            fecha = timezone.datetime.strptime(fecha_filter, '%Y-%m-%d')
            credenciales = credenciales.filter(fecha_subida__date=fecha)
        except ValueError:
            pass  # Si no puede convertir la fecha, no aplicamos el filtro.

    # Ordenar por fecha
    if orden == 'asc':
        credenciales = credenciales.order_by('fecha_subida')
    else:
        credenciales = credenciales.order_by('-fecha_subida')

    # Obtener los oficios disponibles para el filtro
    oficios = Oficio.objects.all()

    return render(request, 'lista_credenciales.html', {
        'credenciales': credenciales,
        'notificaciones': notificaciones,
        'oficios': oficios,
        'oficio_filter': oficio_filter,
        'fecha_filter': fecha_filter,
        'orden': orden,  # Pasamos el valor de 'orden' a la plantilla
    })

    
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.models import User
from Notificaciones.models import  Notification
from Credencial.models import   Credencial

@login_required
def verificar_credencial(request, credencial_id):
    credencial = get_object_or_404(Credencial, id=credencial_id)

    try:
        # Verificar la credencial
        credencial.verificado = True
        credencial.save()

        # Crear una notificación para el técnico
        Notification.objects.create(
            user=credencial.tecnico.user,  # Técnico como destinatario
            message="Tu credencial ha sido verificada y aceptada."
        )
        
        messages.success(request, "La credencial ha sido verificada con éxito.")
    except Exception as e:
        messages.error(request, f"Error al verificar la credencial: {e}")

    # Redirigir de nuevo a la lista de credenciales
    return redirect('Administrador:lista_credenciales')




from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.models import User
from Notificaciones.models import  Notification

@login_required
def rechazar_credencial(request, credencial_id):
    credencial = get_object_or_404(Credencial, id=credencial_id)

    try:
        # Rechazar la credencial (por ejemplo, marcarla como no verificada)
        credencial.verificado = False
        credencial.save()

        # Crear una notificación para el técnico
        Notification.objects.create(
            user=credencial.tecnico.user,  # Técnico como destinatario
            message="Tu credencial ha sido rechazada."
        )
        
        messages.success(request, "La credencial ha sido rechazada con éxito.")
    except Exception as e:
        messages.error(request, f"Error al rechazar la credencial: {e}")

    # Redirigir de nuevo a la lista de credenciales
    return redirect('Administrador:lista_credenciales')



from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from User.models import Localidad
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from Post.models import Publicacion
from Notificaciones.models import Notification  # Asegúrate de importar el modelo correcto


def gestionar_publicaciones(request):
    publicaciones = Publicacion.objects.all()  # Obtener todas las publicaciones

    # Obtener los filtros de la solicitud GET
    ubicacion_id = request.GET.get('ubicacion')  # Filtro por ubicación
    estado = request.GET.get('estado')
    oficio_id = request.GET.get('oficio')  # Filtro por oficio

    # Filtrar por ubicación
    if ubicacion_id:
        publicaciones = publicaciones.filter(ubicacion__icontains=ubicacion_id)  # Filtrar por nombre de ubicación

    # Filtrar por estado
    if estado:
        publicaciones = publicaciones.filter(estado=estado)

    # Filtrar por oficio
    if oficio_id:
        publicaciones = publicaciones.filter(oficios__id=oficio_id)

    # Si es una solicitud POST para cambiar visibilidad, suspender o eliminar una publicación
    if request.method == 'POST':
        accion = request.POST.get('accion')
        publicacion_id = request.POST.get('publicacion_id')
        publicacion = get_object_or_404(Publicacion, id=publicacion_id)

        if accion == 'toggle_visibility':
            publicacion.visible_para_tecnicos = not publicacion.visible_para_tecnicos
            publicacion.save()
        elif accion == 'suspend':
            motivo = request.POST.get('motivo', 'No se especificó un motivo.')
            publicacion.estado = 'suspendida'
            publicacion.visible_para_tecnicos = False
            publicacion.save()
            Notification.objects.create(
                user=publicacion.cliente,
                message=f"Tu publicación '{publicacion.titulo}' ha sido suspendida. Motivo: {motivo}",
            )
        elif accion == 'delete':
            motivo = request.POST.get('motivo', 'No se especificó un motivo.')
            Notification.objects.create(
                user=publicacion.cliente,
                message=f"Tu publicación '{publicacion.titulo}' ha sido eliminada. Motivo: {motivo}",
            )
            publicacion.delete()

        return redirect('Administrador:gestionar_publicaciones')

    # Obtener todas las ubicaciones únicas de las publicaciones (sin duplicados)
    ubicaciones = Publicacion.objects.values('ubicacion').distinct()

    return render(request, 'gestionar_publicacionesadmin.html', {
        'publicaciones': publicaciones,
        'ubicaciones': ubicaciones,  # Pasar las ubicaciones al template
        'oficios': Oficio.objects.all(),
        'estado': estado,
        'ubicacion_id': ubicacion_id,
        'oficio_id': oficio_id,
    })











@login_required
def marcar_como_leida_admin(request, notificacion_id):
    # Verificamos que el usuario sea un administrador
    if not request.user.is_staff:
        return redirect('User:perfil_tecnico')  # O redirigir a la página de acceso denegado
    
    notificacion = get_object_or_404(Notification, id=notificacion_id)
    notificacion.is_read = True
    notificacion.save()
    
    # Redirigir al administrador a donde estaba antes
    return redirect('Administrador:lista_credenciales')

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from User.models import Tecnico


@login_required
def marcar_como_leida_tecnico(request, notificacion_id):
    # Obtén el técnico relacionado con el usuario actual usando select_related
    tecnico = get_object_or_404(Tecnico.objects.select_related('user'), user=request.user)
    notificacion = get_object_or_404(Notification, id=notificacion_id)

    # Verificar que la notificación pertenece al técnico
    if notificacion.user == tecnico.user:
        notificacion.is_read = True
        notificacion.save()

    return redirect('User:perfil_tecnico')




@login_required
def marcar_como_leida_usuario(request, notificacion_id):
    # Verificamos que el usuario sea el propietario de la notificación
    notificacion = get_object_or_404(Notification, id=notificacion_id)
    
    if notificacion.user == request.user:
        notificacion.is_read = True
        notificacion.save()
    
    # Redirigir al usuario a su perfil o la página correspondiente
    return redirect('Post:gestionar_publicaciones')


from django.shortcuts import get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required


@staff_member_required
def eliminar_notificacion(request, notificacion_id):
    # Obtener la notificación
    notificacion = get_object_or_404(Notification, id=notificacion_id)

    # Eliminar la notificación
    notificacion.delete()

    # Redirigir de vuelta a la página de gestión de notificaciones
    return redirect('Administrador:gestionar_publicaciones')

from gestionHistorial.models import GestionHistorial

@staff_member_required
def lista_perfiles(request):
    perfiles = User.objects.all()
    return render(request, 'lista_perfiles.html', {'perfiles': perfiles})

@staff_member_required
def gestionar_perfil(request, usuario_id):
    usuario = get_object_or_404(User, id=usuario_id)

    if request.method == 'POST':
        accion = request.POST.get('accion')
        motivo = request.POST.get('motivo', 'No especificado.')

        if accion == 'suspender':
            usuario.is_active = False
            usuario.save()  # Asegurar que el usuario esté guardado antes de usarlo en otros modelos
            Notification.objects.create(
                user=usuario,
                message=f"Tu cuenta ha sido suspendida. Motivo: {motivo}"
            )
            GestionHistorial.objects.create(
                administrador=request.user, 
                usuario_afectado=usuario, 
                accion='suspendido',
                motivo=motivo
            )
            messages.success(request, f"La cuenta de {usuario.username} fue suspendida.")
        elif accion == 'reactivar':
            usuario.is_active = True
            usuario.save()
            Notification.objects.create(
                user=usuario,
                message="Tu cuenta ha sido reactivada. Puedes volver a usar la plataforma."
            )
            GestionHistorial.objects.create(
                administrador=request.user, 
                usuario_afectado=usuario, 
                accion='reactivado'
            )
            messages.success(request, f"La cuenta de {usuario.username} fue reactivada.")
        elif accion == 'eliminar':
            Notification.objects.create(
                user=usuario,
                message=f"Tu cuenta ha sido eliminada. Motivo: {motivo}"
            )
            GestionHistorial.objects.create(
                administrador=request.user, 
                usuario_afectado=usuario, 
                accion='eliminado',
                motivo=motivo
            )
            usuario.delete()  # Eliminar después de usar el usuario en el historial
            messages.success(request, f"La cuenta de {usuario.username} fue eliminada.")

        return redirect('Administrador:lista_perfiles')

    return render(request, 'gestionar_perfiles.html', {'usuario': usuario})


@staff_member_required
def ver_historial(request):
    historial = GestionHistorial.objects.all().order_by('-fecha')
    return render(request, 'historial_acciones.html', {'historial': historial})


from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render

@staff_member_required
def panel_administrador(request):
    return render(request, 'panel_administrador.html')

from django.shortcuts import render, get_object_or_404, redirect
from Reseñas.models import Reseña
from django.contrib import messages



def panel_administracion_reseñas(request):
    técnicos = User.objects.filter(perfil_tecnico=True)  # Asegúrate de que `profile__is_tecnico` sea correcto
    reseñas = Reseña.objects.all()
    
    # Filtrar por técnico
    if request.GET.get('tecnico'):
        reseñas = reseñas.filter(tecnico_id=request.GET.get('tecnico'))
    
    # Filtrar por calificación
    if request.GET.get('calificacion'):
        reseñas = reseñas.filter(calificacion=request.GET.get('calificacion'))
    
    # Filtrar por fecha
    if request.GET.get('fecha'):
        reseñas = reseñas.filter(fecha__date=request.GET.get('fecha'))
    
    return render(request, 'panel_reseñas.html', {
        'reseñas': reseñas,
        'técnicos': técnicos,
    })



def editar_reseña(request, reseña_id):
    reseña = get_object_or_404(Reseña, id=reseña_id)

    if request.method == 'POST':
        comentario = request.POST.get('comentario', reseña.comentario)
        calificacion = request.POST.get('calificacion', reseña.calificacion)

        # Validar calificación
        if not comentario.strip():
            messages.error(request, "El comentario no puede estar vacío.")
        elif not calificacion.isdigit() or not (1 <= int(calificacion) <= 5):
            messages.error(request, "La calificación debe ser un número entre 1 y 5.")
        else:
            reseña.comentario = comentario
            reseña.calificacion = int(calificacion)
            reseña.save()
            messages.success(request, "Reseña actualizada correctamente.")
            return redirect('Administrador:panel_administracion_reseñas')

    return render(request, 'editar_reseña.html', {'reseña': reseña})

def eliminar_reseña(request, reseña_id):
    reseña = get_object_or_404(Reseña, id=reseña_id)
    if request.method == 'POST':
        cliente = reseña.cliente
        reseña.delete()

        # Enviar notificación al cliente (a implementar)
        messages.success(request, f"Reseña eliminada correctamente y el cliente ha sido notificado.")
        return redirect('Administrador:panel_administracion_reseñas')

    return render(request, 'eliminar_reseña.html', {'reseña': reseña})


from django.shortcuts import render
from django.db.models import Sum
from django.utils.timezone import now
from ventasPremium.models import VentasPremium
from datetime import timedelta

from django.db.models import Sum
from django.shortcuts import render
from datetime import datetime
from ventasPremium.models import VentasPremium
from ventasPublicaciones.models import VentasPublicaciones

def reporte_ventas_premium(request):
    # Obtener el mes actual y el año actual
    mes_actual = datetime.now().month
    año_actual = datetime.now().year
    
    # Filtrar las ventas premium realizadas en el mes actual
    ventas_premium_mes = VentasPremium.objects.filter(fecha__year=año_actual, fecha__month=mes_actual)
    
    # Filtrar las ventas de publicaciones realizadas en el mes actual
    ventas_publicaciones_mes = VentasPublicaciones.objects.filter(fecha__year=año_actual, fecha__month=mes_actual)
    
    # Calcular el total de ventas y el monto total para las ventas premium
    total_ventas_premium = ventas_premium_mes.count()
    total_monto_premium = ventas_premium_mes.aggregate(Sum('cantidad_pago'))['cantidad_pago__sum'] or 0
    
    # Calcular el total de ventas y el monto total para las ventas de publicaciones
    total_ventas_publicaciones = ventas_publicaciones_mes.count()
    total_monto_publicaciones = ventas_publicaciones_mes.aggregate(Sum('monto_pagado'))['monto_pagado__sum'] or 0

    # Preparar los datos para mostrarlos en la plantilla
    context = {
        'ventas_premium_mes': ventas_premium_mes,
        'total_ventas_premium': total_ventas_premium,
        'total_monto_premium': total_monto_premium,
        'ventas_publicaciones_mes': ventas_publicaciones_mes,
        'total_ventas_publicaciones': total_ventas_publicaciones,
        'total_monto_publicaciones': total_monto_publicaciones,
    }
    
    return render(request, 'reporte_ventas_premium.html', context)

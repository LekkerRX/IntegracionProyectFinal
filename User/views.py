from django.shortcuts import render
from django.shortcuts import render, redirect

from django.contrib import messages
from django.shortcuts import redirect

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate

from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login


def pagina_inicio(request):
    # apararecer solo when is_home is false
    is_homepage = True
    return render(request, 'homepagefromhomepage.html', {'is_homepage': is_homepage})


import mercadopago
from django.shortcuts import render, redirect
import mercadopago
from django.shortcuts import render
from django.http import HttpResponseServerError

def premium(request):
    MERCADO_PAGO_ACCESS_TOKEN = 'APP_USR-693148132136597-112817-9219b3273f4db6031cdbed01fb6488d0-2121464661'
    sdk = mercadopago.SDK(MERCADO_PAGO_ACCESS_TOKEN)

    # Configuración de la preferencia
    preference_data = {
        "items": [
            {
                "title": "Suscripción Premium",
                "quantity": 1,
                "unit_price": 7000.0,
                "currency_id": "CLP"
            }
        ],
        "back_urls": {
            "success": "http://127.0.0.1:8000/confirmar-pago-premium",
            "failure": "http://127.0.0.1:8000/confirmar-pago-failure",
            "pending": "http://127.0.0.1:8000/premium/"
        },
        "auto_return": "approved",
        "external_reference": f"pago_premium_usuario_{request.user.id}"
    }

    try:
        preference_response = sdk.preference().create(preference_data)
        print(preference_response)  # Para depuración: muestra la respuesta completa en la consola
        if 'response' in preference_response and 'init_point' in preference_response['response']:
            checkout_url = preference_response['response']['init_point']
            return render(request, 'premium.html', {"checkout_url": checkout_url})
        else:
            return JsonResponse(preference_response, status=500)  # Devuelve la respuesta completa para inspección
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)




def confirmar_pago_failure(request):
    # Obtener parámetros de la URL
    external_reference = request.GET.get('external_reference')
    payment_status = request.GET.get('status')  # Estado del pago enviado por Mercado Pago

    if not external_reference or not payment_status:
        return JsonResponse({"error": "Falta la referencia externa o el estado del pago."}, status=400)

    try:
        # Si el estado del pago no es aprobado, mostramos un mensaje de error
        if payment_status != 'approved':
            # Mostrar el mensaje de error en el perfil del técnico
            messages.error(request, "El pago no fue aprobado. Por favor, intenta nuevamente.")
            return redirect('User:perfil_tecnico')
        
        # Si el pago fue aprobado (en este caso, no se realizaría, pero puedes incluir lógica adicional si fuera necesario)
        return redirect('User:perfil_tecnico')

    except Exception as e:
        # Si ocurre algún otro error, devolver un mensaje genérico
        messages.error(request, f"Hubo un error al procesar el pago: {str(e)}")
        return redirect('User:perfil_tecnico')




import mercadopago
from django.shortcuts import redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from User.models import Tecnico  # Asegúrate de que este modelo sea el correcto.

from datetime import timedelta
from ventasPremium.models import VentasPremium

@login_required
def confirmar_pago_premium(request):
    # Obtener parámetros de la URL
    external_reference = request.GET.get('external_reference')
    payment_status = request.GET.get('status')  # Estado del pago enviado por Mercado Pago

    if not external_reference or not payment_status:
        return JsonResponse({"error": "Falta la referencia externa o el estado del pago."}, status=400)

    try:
        # Verificar si el estado del pago es aprobado
        if payment_status != 'approved':
            return JsonResponse({"error": "El pago no fue aprobado."}, status=400)
        
        # Actualizar el estado de premium en el modelo Técnico
        tecnico = Tecnico.objects.get(user=request.user)  # Suponemos que el técnico está relacionado con el usuario autenticado
        tecnico.es_premium = True
        tecnico.save()

        # Registrar la venta premium
        VentasPremium.objects.create(
            tecnico=request.user,
            cantidad_pago=50.0,  # El precio fijo del premium
        )

        # Redirigir a la página de perfil con un mensaje de éxito
        return redirect('User:perfil_tecnico')
    except Tecnico.DoesNotExist:
        return JsonResponse({"error": "El usuario autenticado no es un técnico."}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)




from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import TecnicoForm,EditProfileForm
from .models import Tecnico







from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login



from django.contrib.auth import get_user_model

# views.py
from django.shortcuts import render



from django.contrib.auth import logout
from django.shortcuts import render

def pagina_tecnico(request):
    if request.user.is_authenticated:  # Verifica si el usuario está autenticado
        logout(request)  # Cierra la sesión del usuario
    return render(request, 'HomepageTecnic.html')



def pagina_cliente(request):
    return render(request, 'HomepageClient.html')

from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth import login
from django.core.exceptions import PermissionDenied
from .forms import ClientLoginForm  # Asegúrate de tener el formulario

def client_login_client(request):
    if request.user.is_authenticated:
        return redirect('Post:gestionar_publicaciones')

    form = ClientLoginForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        
        if user:
            # Verificar si la cuenta está suspendida
            if not user.is_active:
                # Mostrar el mensaje de que la cuenta está suspendida
                messages.error(request, f"Esta cuenta está suspendida.")
                return render(request, 'HomepageClient.html', {'form': form})

            # Si la cuenta está activa, proceder con el inicio de sesión
            login(request, user)
            return redirect('Post:gestionar_publicaciones')

    return render(request, 'HomepageClient.html', {'form': form})


# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import EmailAuthenticationForm

from django.contrib.auth import authenticate, login

def custom_login(request):
    if request.user.is_authenticated:
        return redirect('User:perfil_tecnico')

    form = EmailAuthenticationForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            # Especificamos el backend para la autenticación de los técnicos
            user = authenticate(request=request, email=form.cleaned_data['email'], password=form.cleaned_data['password'], backend='User.authentication_backend.CustomBackend')
            
            if user is not None:
                login(request, user, backend='User.authentication_backend.CustomBackend')
                return redirect('User:perfil_tecnico')
            else:
                form.add_error(None, "Correo o contraseña inválidos.")

    return render(request, 'HomepageTecnic.html', {'form': form})


# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import ClientLoginForm


from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import ClientLoginForm  # Asegúrate de tener el formulario de cliente adecuado

# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import ClientLoginForm

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import ClientLoginForm

from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import ClientLoginForm

from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import ClientLoginForm

def client_login_client(request):
    if request.user.is_authenticated:
        return redirect('Post:gestionar_publicaciones')

    form = ClientLoginForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        if user:
            login(request, user)
            return redirect('Post:gestionar_publicaciones')

    return render(request, 'HomepageClient.html', {'form': form})








from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Tecnico  # Asegúrate de importar tu modelo
from .forms import ImagenPerfilForm  # Formulario para subir imagen (si es necesario)
from django.shortcuts import render, get_object_or_404, redirect
from .forms import ImagenPerfilForm
from .models import Tecnico
from django.contrib.auth import logout


def custom_logout(request):
    logout(request)  # Cierra la sesión del usuario
    return redirect('User:pagina_inicio')  # Redirige a la página de inicio de sesión



from django.shortcuts import render
from Post.models import Publicacion
from django.contrib.auth.decorators import login_required
from Notificaciones.models import Notification
from django.db import models

@login_required
def publicaciones_tecnico(request):
    try:
        tecnico = Tecnico.objects.get(user=request.user)
    except Tecnico.DoesNotExist:
        return {'message': 'No se encontró el perfil de técnico.'}

    oficios_tecnico = tecnico.oficios.all()
    publicaciones = Publicacion.objects.filter(oficios__in=oficios_tecnico).distinct()  # Aquí agregamos distinct()

    # Filtro de favoritos
    mostrar_favoritos = request.GET.get('favoritos', 'false') == 'true'
    if mostrar_favoritos:
        publicaciones = publicaciones.filter(favoritos__user=request.user)

    # Agregar información de favoritos
    publicaciones = publicaciones.annotate(
        es_favorito=models.Exists(
            Favorito.objects.filter(user=request.user, publicacion=models.OuterRef('pk'))
        )
    )

    # Ordenación por fecha
    sort = request.GET.get('sort', 'desc')
    if sort == 'asc':
        publicaciones = publicaciones.order_by('fecha_publicacion')
    else:
        publicaciones = publicaciones.order_by('-fecha_publicacion')

    comunas = Publicacion.objects.values_list('ubicacion', flat=True).distinct()

    return render(request, 'publicaciones_tecnico.html', {
        'publicaciones': publicaciones,
        'sort': sort,
        'comunas': comunas,
        'mostrar_favoritos': mostrar_favoritos,
    })




from django.shortcuts import get_object_or_404, render, redirect

from .forms import ReseñaForm  # Asegúrate de tener este formulario creado
from django.db.models import Avg

def perfil_tecnico_cliente(request, id):
    # Obtener el técnico por su id
    tecnico = get_object_or_404(Tecnico, id=id)
    
    # Buscar las reseñas asociadas al técnico en la tabla Reseñas_reseña
    reseñas = Reseña.objects.filter(tecnico=tecnico).order_by('-fecha')  # Filtramos las reseñas por el técnico
    
    promedio_calificacion = reseñas.aggregate(Avg('calificacion'))['calificacion__avg'] or 0
    # Procesar las estrellas de cada reseña
    for reseña in reseñas:
        reseña.estrellas = [i for i in range(reseña.calificacion)]  # Crear lista de estrellas

    # Si el cliente está autenticado y quiere editar una reseña
    if request.method == 'POST':
        reseña_id = request.POST.get('reseña_id')
        reseña = Reseña.objects.get(id=reseña_id)

        if reseña.cliente == request.user:
            form = ReseñaForm(request.POST, instance=reseña)
            if form.is_valid():
                form.save()
                return redirect('User:perfil_tecnico_cliente', id=tecnico.id)  # Redirigir al perfil del técnico
    else:
        form = None

    # Obtener los días y horas de trabajo del técnico
    dias_trabajo = tecnico.horario_disponible.split(' desde ')[0].split(', ') if tecnico.horario_disponible else []
    hora_inicio = tecnico.horario_disponible.split('desde las ')[1].split(' hasta ')[0] if 'desde' in tecnico.horario_disponible else ''
    hora_fin = tecnico.horario_disponible.split('hasta las ')[1] if 'hasta' in tecnico.horario_disponible else ''
    
    # Limpiar la cadena para obtener solo los nombres de las comunas
    if tecnico.localidades:
        localidades_str = tecnico.localidades
        localidades_nombres = [
            loc.strip().split(': ')[1].replace('>', '') if ': ' in loc else loc.strip()
            for loc in localidades_str.replace("<QuerySet [", "").replace("]>", "").split(', ') if loc.strip()
        ]
    else:
        localidades_nombres = []

    # Procesar el horario para enviarlo al template
    horarios = []
    if tecnico.horario_disponible:
        partes = tecnico.horario_disponible.split(' desde ')
        dias = partes[0].split(', ')
        horas = partes[1].strip() if len(partes) > 1 else None
        for dia in dias:
            horarios.append({'dia': dia.strip(), 'horas': horas})

    # Acceder al email del técnico a través de la relación con el modelo User
    email_tecnico = tecnico.user.email

    context = {
        'tecnico': tecnico,  # El objeto 'tecnico' entero se pasa para poder acceder a todos sus atributos
        'localidades': localidades_nombres,  # Lista de localidades que el técnico cubre
        'horarios': horarios,  # Lista de horarios disponibles
        'nombre_tecnico': tecnico.nombre.title() if tecnico.nombre else '',  # Nombre del técnico, capitalizado
        'email_tecnico': email_tecnico,  # Email del técnico ahora correctamente obtenido
        'especialidades': tecnico.oficios.all(),  # Especialidades del técnico
        'imagen_tecnico': tecnico.imagen_perfil.url if tecnico.imagen_perfil else 'default_profile_image_url',  # Imagen de perfil (si existe)
        'reseñas': reseñas,  # Pasa las reseñas al template
        'form': form,  # Pasa el formulario al template
        'promedio_calificacion': promedio_calificacion,
    }

    return render(request, 'visitPerfil.html', context)




from Chat.models import Chat


@login_required
def perfil_tecnico(request):
    tecnico = get_object_or_404(Tecnico, user=request.user)
    
  
    reseñas = Reseña.objects.filter(tecnico=tecnico).order_by('-fecha')  
    promedio_calificacion = reseñas.aggregate(Avg('calificacion'))['calificacion__avg'] or 0
    
    # Actualizar el campo `calificacion_promedio` del técnico
    tecnico.calificacion_promedio = promedio_calificacion
    tecnico.save()
    
    # Procesar las estrellas de cada reseña
    for reseña in reseñas:
        reseña.estrellas = [i for i in range(reseña.calificacion)]  # Crear lista de estrellas
        
    

    
   
    
    user = User.objects.get(id=tecnico.user.id)
    
 
    dias_trabajo = tecnico.horario_disponible.split(' desde ')[0].split(', ') if tecnico.horario_disponible else []
    hora_inicio = tecnico.horario_disponible.split('desde las ')[1].split(' hasta ')[0] if 'desde' in tecnico.horario_disponible else ''
    hora_fin = tecnico.horario_disponible.split('hasta las ')[1] if 'hasta' in tecnico.horario_disponible else ''
    
    # Limpiar la cadena para obtener solo los nombres de las comunas
    if tecnico.localidades:
        localidades_str = tecnico.localidades
        cleaned_str = localidades_str.replace("<QuerySet [", "").replace("]>", "")
        localidades_nombres = [
            loc.strip().split(': ')[1].replace('>', '') if ': ' in loc else loc.strip()  # Solo divide si contiene ': '
            for loc in cleaned_str.split(', ') if loc.strip()
        ]
    else:
        localidades_nombres = []

    # Procesar el horario para enviarlo al template
    horarios = []
    horas = None
    if tecnico.horario_disponible:
        partes = tecnico.horario_disponible.split(' desde ')
        dias = partes[0].split(', ')
        if len(partes) > 1:
            horas = partes[1].strip()
        for dia in dias:
            horarios.append({'dia': dia.strip(), 'horas': horas})

    # Obtener las notificaciones del técnico (usuario)
    notificaciones = Notification.objects.filter(user=request.user, is_read=False)

    # Obtener los chats activos del técnico
    chats_activos = Chat.objects.filter(tecnico=request.user)

    if request.method == 'POST':
        form = ImagenPerfilForm(request.POST, request.FILES, instance=tecnico)
        if form.is_valid():
            # Actualiza el técnico
            form.save()

            # Actualiza el correo en auth_user
            user.email = form.cleaned_data['correo']
            user.save()

            messages.success(request, 'Perfil actualizado exitosamente.')
            return redirect('User:perfil_tecnico')  # Redirige a la página de perfil u otra
        else:
            messages.error(request, 'Hubo un error al actualizar el perfil. Inténtalo de nuevo.')
    else:
        form = ImagenPerfilForm(initial={
            'correo': user.email,  # Cargar el correo desde auth_user
            'nombre': tecnico.nombre,
            'horario_disponible': tecnico.horario_disponible,
            'dias_trabajo': dias_trabajo,
            'hora_inicio': hora_inicio,
            'hora_fin': hora_fin,
        })

    context = {
        'tecnico': tecnico,
        'tecnico_id':tecnico.id,
        'email': request.user.email,
        'form': form,
        'localidades': localidades_nombres,
        'horarios': horarios,
        'nombre_tecnico': tecnico.nombre.title() if tecnico.nombre else '',  # Mayúsculas independiente de BD
        'notificaciones': notificaciones,  # Añadir las notificaciones al contexto
        'chats_activos': chats_activos,  # Añadir los chats activos del técnico
        'reseñas': reseñas,  # Añadir las reseñas al contexto
        'promedio_calificacion':promedio_calificacion
    }
    
    return render(request, 'perfilTecnico.html', context)





from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import TecnicoForm
from django.db import IntegrityError


def registro_tecnico(request):
    if request.method == 'POST':
        form = TecnicoForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # Crear el usuario
                user = User(
                    username=form.cleaned_data['nombre'],
                    email=form.cleaned_data['email']
                )
                user.set_password(form.cleaned_data['password1'])
                user.save()

                # Crear el perfil de Técnico
                tecnico = form.save(commit=False)
                tecnico.user = user

                # Guardar días y horas disponibles
                dias_seleccionados = ', '.join(form.cleaned_data['dias_trabajo'])
                tecnico.horario_disponible = f"{dias_seleccionados} desde las {form.cleaned_data['hora_inicio']} hasta las {form.cleaned_data['hora_fin']}"
                tecnico.save()

                # Guardar la relación Many-to-Many de oficios
                tecnico.oficios.set(form.cleaned_data['oficios'])

                # Guardar las localidades
                tecnico.localidades = ', '.join(str(localidad) for localidad in form.cleaned_data['localidades'])
                tecnico.save()

                return redirect('User:pagina_inicio')

            except IntegrityError as e:
                # Captura la excepción de clave duplicada y muestra un mensaje amigable
                if 'auth_user_username_key' in str(e):  # Verifica que la excepción sea por nombre de usuario duplicado
                    messages.error(request, "Este nombre de usuario ya está ocupado. Por favor, elige otro.")
                else:
                    messages.error(request, f"Error al registrar: {e}")
            except Exception as e:
                # Captura otras excepciones generales
                messages.error(request, f"Error al registrar: {e}")
        else:
            # Si el formulario tiene errores, agregarlos a los mensajes
            for field in form:
                for error in field.errors:
                    messages.error(request, error)
    else:
        form = TecnicoForm()

    return render(request, 'register.html', {'form': form})





from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ClientRegistrationForm

# views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from .forms import ClientRegistrationForm

from django.contrib.auth import login
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from .forms import ClientRegistrationForm


from django.contrib.auth import login
from django.contrib.auth.backends import ModelBackend  # Importa el backend que prefieras

def client_register(request):
    if request.user.is_authenticated:
        return redirect('User:login_client')  # Redirigir si ya está autenticado

    if request.method == 'POST':
        form = ClientRegistrationForm(request.POST)
        if form.is_valid():
            try:
                # Crear el usuario
                user = User(
                    username=form.cleaned_data['username'],
                    email=form.cleaned_data['email']
                )
                user.set_password(form.cleaned_data['password1'])
                user.save()

                # Autenticar y redirigir, especificando el backend
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                messages.success(request, "¡Registro exitoso!")
                return redirect('User:login_client')  # Redirigir a la página de inicio o perfil
            except Exception as e:
                messages.error(request, f"Error al registrar el cliente: {e}")
    else:
        form = ClientRegistrationForm()

    return render(request, 'register_client.html', {'form': form})


from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from Post.models import Publicacion
from Aceptaciones.models import Aceptacion
from Notificaciones.models import Notification  # Importamos el modelo de notificaciones

@login_required
def postular_publicacion(request, publicacion_id):
    publicacion = get_object_or_404(Publicacion, id=publicacion_id)

    # Verifica que el usuario sea un técnico
    try:
        tecnico = request.user.perfil_tecnico  # Accede al perfil de técnico usando el related_name
    except Tecnico.DoesNotExist:
        messages.error(request, "Solo los técnicos pueden postularse a publicaciones.")
        return redirect('User:publicaciones_tecnico')

    # Verifica que el técnico no haya postulado previamente
    if Aceptacion.objects.filter(tecnico=tecnico, publicacion=publicacion).exists():
        messages.warning(request, "Ya has postulado a esta publicación.")
        return redirect('User:publicaciones_tecnico')

    # Crear la aceptación
    Aceptacion.objects.create(tecnico=tecnico, publicacion=publicacion)

    # Cambiar el estado de la publicación a "Atendida por un técnico"
    publicacion.estado = 'Publicación Atendida'  
    publicacion.save()

    # Ocultar publicación para otros técnicos
    publicacion.visible_para_tecnicos = False
    publicacion.save()

    # Crear una notificación para el cliente
    Notification.objects.create(
        user=publicacion.cliente,  # Usuario al que va dirigida la notificación
        message=f"El técnico {tecnico.nombre} ha postulado a tu publicación '{publicacion.titulo}' y ha comenzado a atenderla."
    )

    # Redirigir a la comunicación con el cliente
    messages.success(request, "Has postulado exitosamente. Ahora espera la respuesta del Cliente.")
    return redirect('User:publicaciones_tecnico')


from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from Favoritos.models import Favorito

@login_required
def toggle_favorito(request, publicacion_id):
    publicacion = get_object_or_404(Publicacion, id=publicacion_id)
    favorito, creado = Favorito.objects.get_or_create(user=request.user, publicacion=publicacion)

    if not creado:  # Si ya existía, eliminar el favorito
        favorito.delete()
        es_favorito = False
    else:
        es_favorito = True

    return JsonResponse({'es_favorito': es_favorito})

from django.shortcuts import redirect
from firebase_admin import db

from django.http import JsonResponse
from django.shortcuts import render, redirect
from firebase_admin import db
import mercadopago

from django.shortcuts import redirect
from firebase_admin import db
import mercadopago
from django.http import JsonResponse
from .models import Tecnico
import mercadopago



def crear_preferencia(request, tecnico_id, publicacion_id, chat_id):
    try:
        # Obtener el técnico por ID
        tecnico = get_object_or_404(Tecnico, id=tecnico_id)
        
        # Obtener la publicación por ID
        publicacion = get_object_or_404(Publicacion, id=publicacion_id)
        
        

        # Verificar que el técnico tenga un access_token
        if not tecnico.access_token:
            return JsonResponse({"error": "El técnico no tiene un access_token asociado."}, status=400)
        
        # Verificar el monto máximo establecido por el cliente
        if not publicacion.limite_monto or publicacion.limite_monto <= 0:
            return JsonResponse({"error": "El monto máximo de la publicación no es válido."}, status=400)

        # Configurar el cliente de Mercado Pago con el access_token del técnico
        sdk = mercadopago.SDK(tecnico.access_token)

        # Crear la preferencia de pago
        preference_data = {
            "items": [
                {
                    "title": f"Pago por servicio técnico - Publicación {publicacion.id}",
                    "quantity": 1,
                    "unit_price": float(publicacion.limite_monto),  
                    "currency_id": "CLP",
                }
            ],
            "back_urls": {
                "success": "http://127.0.0.1:8000/confirmar-pago",
                "failure": "http://127.0.0.1:8000/confirmar-pago-failure-publicacion",
                "pending": "https://miweb.com/pending",
            },
            "auto_return": "approved",
            "payer": {
                "email": tecnico.user.email,  # Correo del técnico
            },
            "external_reference": f"pago_tecnico_{tecnico_id}_publicacion_{publicacion_id}_chat_id_{chat_id}",
        }

        # Crear la preferencia en Mercado Pago
        response = sdk.preference().create(preference_data)

        # Obtener el link del checkout
        init_point = response["response"]["init_point"]

        return JsonResponse({"checkout_url": init_point}, status=200)

    except (Tecnico.DoesNotExist, Publicacion.DoesNotExist):
        return JsonResponse({"error": "El técnico o la publicación no existe."}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)





from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from ventasPublicaciones.models import VentasPublicaciones
import mercadopago
from firebase_admin import db
from datetime import datetime

def confirmar_pago(request):
    # Obtener el parámetro 'external_reference' de la URL
    external_reference = request.GET.get('external_reference')
    payment_status = request.GET.get('status')  # Se asume que MercadoPago pasa un parámetro 'status'

    if not external_reference or not payment_status:
        return JsonResponse({"error": "Chat ID o estado de pago no proporcionado."}, status=400)

    # Extraer el chat_id del external_reference
    try:
        # Obtener el chat_id de la cadena 'pago_tecnico_{tecnico_id}_publicacion_{publicacion_id}_chat_id_{chat_id}'
        chat_id = external_reference.split('chat_id_')[-1]
    except IndexError:
        return JsonResponse({"error": "El chat_id no se pudo extraer de la referencia externa."}, status=400)

    try:
        # Verificar si el estado del pago es aprobado
        if payment_status != 'approved':
            return JsonResponse({"error": "El pago no fue aprobado."}, status=400)

        # Obtener la publicación y el técnico asociados al pago
        tecnico_id = external_reference.split('pago_tecnico_')[1].split('_publicacion')[0]
        publicacion_id = external_reference.split('_publicacion_')[1].split('_chat_id')[0]
        tecnico = get_object_or_404(Tecnico, id=tecnico_id)
        publicacion = get_object_or_404(Publicacion, id=publicacion_id)

        # Verificar que el monto pagado coincide con el límite de la publicación
        if publicacion.limite_monto:
            monto_pagado = float(publicacion.limite_monto)
        else:
            return JsonResponse({"error": "El monto máximo de la publicación no está definido."}, status=400)

        # Guardar la venta en el modelo VentasPublicaciones
        venta = VentasPublicaciones(
            publicacion=publicacion,
            monto_pagado=monto_pagado,
            tecnico=tecnico,
            cliente=tecnico.user,  # Suponiendo que el cliente es el usuario asociado al técnico
            fecha=datetime.now()  # La fecha y hora actual
        )
        venta.save()

        # Conectar a la base de datos de Firebase
        chat_ref = db.reference(f"chats/{chat_id}")

        # Actualizar el estado del chat a 'pagado: true'
        chat_ref.update({
            "pagado": True
        })

        # Redirigir al chat con el chat_id
        return redirect(f"/Chat/{chat_id}")  # Redirigir al chat con el chat_id

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)



@login_required
def confirmar_pago_failure_publicacion(request):
    # Obtener los parámetros de la URL
    external_reference = request.GET.get('external_reference')
    payment_status = request.GET.get('status')  # Estado del pago enviado por Mercado Pago

    if not external_reference or not payment_status:
        return JsonResponse({"error": "Falta la referencia externa o el estado del pago."}, status=400)

    try:
        # Extraer el chat_id del external_reference
        try:
            chat_id = external_reference.split('chat_id_')[-1]
        except IndexError:
            return JsonResponse({"error": "El chat_id no se pudo extraer de la referencia externa."}, status=400)

        # Si el estado del pago no es aprobado, mostramos un mensaje de error en el chat
        if payment_status != 'approved':
            # Mostrar el mensaje de error en el chat con el chat_id
            messages.error(request, "El pago no fue aprobado. Por favor, intenta nuevamente.")
            return redirect(f"/Chat/{chat_id}")  # Redirigir al chat correspondiente con el chat_id

        # Si el pago fue aprobado (en este caso no se realizaría, pero puedes incluir lógica adicional si fuera necesario)
        return redirect(f"/Chat/{chat_id}")  # Redirigir al chat correspondiente

    except Exception as e:
        # Si ocurre algún otro error, devolver un mensaje genérico
        messages.error(request, f"Hubo un error al procesar el pago: {str(e)}")
        return redirect(f"/Chat/{chat_id}")  # Redirigir al chat correspondiente con el chat_id


# views.py
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse
from .models import Tecnico
from Reseñas.models import Reseña



from django.contrib import messages

from django.contrib import messages

def dejar_resena(request, tecnico_id):
    if request.method == 'POST':
        # Buscar al técnico
        tecnico = get_object_or_404(Tecnico, id=tecnico_id)
        
        # Verificar si el cliente ya ha dejado una reseña para este técnico
        if Reseña.objects.filter(cliente=request.user, tecnico=tecnico).exists():
            # Si ya dejó una reseña, mostrar un mensaje y redirigir al perfil del técnico
            messages.info(request, "Ya has enviado una reseña para este técnico anteriormente.")
            return redirect('User:perfil_tecnico_cliente', id=tecnico.id)

        # Obtener la calificación y comentario del formulario
        calificacion = request.POST.get('calificacion')
        comentario = request.POST.get('comentario')
        
        # Crear la reseña
        Reseña.objects.create(
            tecnico=tecnico,
            cliente=request.user,  # Asumiendo que el cliente está autenticado
            calificacion=calificacion,
            comentario=comentario,
            publicacion_id=request.POST.get('publicacion_id')  # Asegúrate de que el formulario pase este valor
        )

        # Enviar mensaje de éxito solo si la reseña fue creada
        messages.success(request, "Has enviado una reseña para este técnico correctamente.")

        # Redirigir al perfil del técnico después de dejar la reseña
        return redirect('User:perfil_tecnico_cliente', id=tecnico.id)
    
    else:
        return HttpResponse("Método no permitido", status=405)
    


import logging
from django.shortcuts import get_object_or_404, redirect

# Configuración básica del logger
logger = logging.getLogger(__name__)

def guardar_reseña(request):
    # Asegurarse de que el cliente está autenticado
    if not request.user.is_authenticated:
        logger.warning('Usuario no autenticado al intentar guardar reseña.')
        return redirect('login')  # Redirige si no está autenticado

    # Obtener el ID de la reseña desde el formulario
    reseña_id = request.POST.get('reseña_id')
    logger.info(f'ID de reseña recibido: {reseña_id}')

    try:
        reseña = get_object_or_404(Reseña, id=reseña_id)
        logger.info(f'Reseña encontrada: {reseña}')
    except Exception as e:
        logger.error(f'Error al obtener la reseña con ID {reseña_id}: {str(e)}')
        return redirect('User:perfil_tecnico_cliente', id=request.POST.get('tecnico_id'))

    # Verificar que el cliente autenticado es el mismo que escribió la reseña
    if reseña.cliente != request.user:
        logger.warning(f'El cliente {request.user} intentó editar una reseña que no le pertenece.')
        return redirect('User:perfil_tecnico_cliente', id=reseña.tecnico.id)  # Redirige si no tiene permiso

    # Crear un formulario de reseña con los datos del POST
    form = ReseñaForm(request.POST, instance=reseña)

    # Verificar si el formulario es válido
    if form.is_valid():
        logger.info('Formulario válido. Guardando la reseña...')
        form.save()  # Guardar los cambios en la reseña
        logger.info('Reseña guardada correctamente.')
        return redirect('User:perfil_tecnico_cliente', id=reseña.tecnico.id)  # Redirigir al perfil del técnico
    else:
        logger.error(f'Formulario inválido. Errores: {form.errors}')
        # Si el formulario no es válido, redirigir de nuevo al perfil
        return redirect('User:perfil_tecnico_cliente', id=reseña.tecnico.id)


from django.shortcuts import render
from .models import Tecnico

def ranking_tecnicos(request):
    # Obtener todos los técnicos con calificación superior a 0, ordenados por calificación promedio (de mayor a menor)
    tecnicos = Tecnico.objects.filter(calificacion_promedio__gt=0).order_by('-calificacion_promedio')

    context = {
        'tecnicos': tecnicos,
    }
    return render(request, 'ranking_tecnicos.html', context)




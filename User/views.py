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
    publicaciones = Publicacion.objects.filter(oficios__in=oficios_tecnico)

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



def perfil_tecnico_cliente(request, id):
    # Obtener el técnico por su id
    tecnico = get_object_or_404(Tecnico, id=id)
    
    # Obtener los días y horas de trabajo del técnico
    dias_trabajo = tecnico.horario_disponible.split(' desde ')[0].split(', ') if tecnico.horario_disponible else []
    hora_inicio = tecnico.horario_disponible.split('desde las ')[1].split(' hasta ')[0] if 'desde' in tecnico.horario_disponible else ''
    hora_fin = tecnico.horario_disponible.split('hasta las ')[1] if 'hasta' in tecnico.horario_disponible else ''
    
    # Limpiar la cadena para obtener solo los nombres de las comunas
    if tecnico.localidades:
        localidades_str = tecnico.localidades
        # Asegurarse de que la cadena esté limpia antes de procesar
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
    email_tecnico = tecnico.user.email  # Corregido para obtener el email desde el modelo User

    context = {
        'tecnico': tecnico,  # El objeto 'tecnico' entero se pasa para poder acceder a todos sus atributos
        'localidades': localidades_nombres,  # Lista de localidades que el técnico cubre
        'horarios': horarios,  # Lista de horarios disponibles
        'nombre_tecnico': tecnico.nombre.title() if tecnico.nombre else '',  # Nombre del técnico, capitalizado
        'email_tecnico': email_tecnico,  # Email del técnico ahora correctamente obtenido
        'especialidades': tecnico.oficios.all(),  # Especialidades del técnico
        'imagen_tecnico': tecnico.imagen_perfil.url if tecnico.imagen_perfil else 'default_profile_image_url',  # Imagen de perfil (si existe)
  
    }

    return render(request, 'visitPerfil.html', context)


from Chat.models import Chat


@login_required
def perfil_tecnico(request):
    tecnico = get_object_or_404(Tecnico, user=request.user)
    user = User.objects.get(id=tecnico.user.id)
    
    # Suponiendo que tienes una forma de obtener los días y horas de trabajo
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
        'email': request.user.email,
        'form': form,
        'localidades': localidades_nombres,
        'horarios': horarios,
        'nombre_tecnico': tecnico.nombre.title() if tecnico.nombre else '',  # Mayúsculas independiente de BD
        'notificaciones': notificaciones,  # Añadir las notificaciones al contexto
        'chats_activos': chats_activos,  # Añadir los chats activos del técnico
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

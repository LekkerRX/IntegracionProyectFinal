from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import CredencialForm
from Notificaciones.models import Notification  # Asegúrate de tener este modelo importado

@login_required
def subir_credencial(request):
    if request.method == 'POST':
        form = CredencialForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # Guardar la credencial
                credencial = form.save(commit=False)
                credencial.tecnico = request.user.perfil_tecnico  # Relacionar con el técnico actual
                credencial.save()

                # Crear una notificación para el administrador
                # Aquí debes enviar la notificación al usuario con rol de administrador
                # Obtener los administradores (puedes hacerlo mediante un rol o grupo específico)
                administradores = User.objects.filter(is_staff=True)  # Ejemplo de filtrado por admin
                for admin in administradores:
                    Notification.objects.create(
                        user=admin,  # Enviar la notificación al administrador
                        message=f"El técnico {credencial.tecnico.nombre} ha postulado una nueva credencial."
                    )

                # Mostrar mensaje de éxito
                messages.success(request, "La credencial se subió correctamente.")
                return redirect('User:perfil_tecnico')  # Redirigir al perfil del técnico después de la subida

            except Exception as e:
                # Si ocurre un error al guardar
                messages.error(request, f"Ocurrió un problema al subir la credencial: {e}")
        else:
            messages.error(request, "Hubo un error con el formulario. Por favor, verifique los datos.")
    else:
        form = CredencialForm()

    return render(request, 'credenciales.html', {'form': form})


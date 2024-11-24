from django.db import models
from django.contrib.auth.models import User

class GestionHistorial(models.Model):
    administrador = models.ForeignKey(User, on_delete=models.CASCADE, related_name="acciones_realizadas")
    usuario_afectado = models.ForeignKey(User, on_delete=models.CASCADE, related_name="acciones_recibidas")
    accion = models.CharField(max_length=50)  # "suspendido", "eliminado", "reactivado", "editado"
    motivo = models.TextField(blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.administrador} realizó {self.accion} sobre {self.usuario_afectado} el {self.fecha}"

from django.db import models
from django.contrib.auth.models import User
from User.models import Tecnico
from Post.models import Publicacion

class Reseña(models.Model):
    cliente = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reseñas_cliente")
    tecnico = models.ForeignKey(Tecnico, on_delete=models.CASCADE, related_name="reseñas_tecnico")
    publicacion = models.ForeignKey(Publicacion, on_delete=models.CASCADE)  # Ajusta la app según tu proyecto
    calificacion = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])  # Calificación de 1 a 5
    comentario = models.TextField(max_length=500, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"Reseña de {self.cliente} a {self.tecnico} - {self.calificacion}/5"

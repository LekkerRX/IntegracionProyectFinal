from django.db import models
from django.contrib.auth.models import User
from Post.models import Publicacion

class Favorito(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favoritos')
    publicacion = models.ForeignKey(Publicacion, on_delete=models.CASCADE, related_name='favoritos')
    marcado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'publicacion')  # Evitar duplicados

    def __str__(self):
        return f"{self.user.username} - {self.publicacion.titulo}"

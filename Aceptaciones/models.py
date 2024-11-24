from django.db import models

# Create your models here.
from django.db import models
from User.models import Tecnico
from Post.models import Publicacion

class Aceptacion(models.Model):
    tecnico = models.ForeignKey(Tecnico, on_delete=models.CASCADE)
    publicacion = models.ForeignKey(Publicacion, on_delete=models.CASCADE)
    fecha_aceptacion = models.DateTimeField(auto_now_add=True)

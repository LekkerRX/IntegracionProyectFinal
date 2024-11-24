from django.db import models
from django.contrib.auth.models import User
import json
from Oficio.models import Oficio
# MODELO USUARIO, ID SE GENERA SOLA POR DJANGO
# IMPORTAMOS USER DE DJANGO

from django.db import models
from django.contrib.auth.models import User



class Localidad(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = 'Localidad'
        verbose_name_plural = 'Localidades'
        ordering = ['nombre']  # Ordenar por nombre de forma ascendente


class Tecnico(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil_tecnico')
    nombre = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=100)
    horario_disponible = models.CharField(max_length=100)
    credenciales_tecnico = models.FileField(upload_to='credenciales/', blank=True, null=True)
    calificacion_promedio = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    oficios = models.ManyToManyField(Oficio, related_name='tecnicos', blank=True)
    localidades = models.CharField(max_length=200, help_text="Localidades en las que opera")
    validado = models.BooleanField(default=False)
    imagen_perfil = models.ImageField(upload_to='imagenes_perfil/', default='imagenes_perfil/default-profile.png')  # Campo para la imagen de perfil

    def __str__(self):
        return f"{self.nombre} - {self.ubicacion}"
    
    class Meta:
        db_table = 'user_tecnico'

    class Meta:
        verbose_name = "Técnico"
        verbose_name_plural = "Técnicos"
        
        



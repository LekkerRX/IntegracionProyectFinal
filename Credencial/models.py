from django.db import models
from User.models import Tecnico
from Oficio.models import Oficio
# Create your models here.
class Credencial(models.Model):
    tecnico = models.ForeignKey(Tecnico, on_delete=models.CASCADE, related_name='credenciales')
    oficio = models.ForeignKey(Oficio, on_delete=models.CASCADE, related_name='credenciales', null=True)
    documento = models.FileField(upload_to='credenciales/', null=True, blank=True)
    fecha_subida = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    verificado = models.BooleanField(default=False)

    def __str__(self):
        return f"Credencial de {self.tecnico.nombre} para {self.oficio.nombre}"

    class Meta:
        verbose_name = "Credencial"
        verbose_name_plural = "Credenciales"

from django.db import models

class Oficio(models.Model):
    codigo = models.CharField(max_length=50, unique=True, verbose_name="Código del Oficio")
    nombre = models.CharField(max_length=255, verbose_name="Nombre del Oficio")

    class Meta:
        verbose_name = "Oficio"
        verbose_name_plural = "Oficios"

    def __str__(self):
        return self.nombre

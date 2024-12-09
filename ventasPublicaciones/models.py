from django.db import models
from django.contrib.auth.models import User
from Post.models import Publicacion 
from User.models import Tecnico

class VentasPublicaciones(models.Model):
    publicacion = models.ForeignKey(Publicacion, on_delete=models.CASCADE, related_name='ventas')
    monto_pagado = models.DecimalField(max_digits=10, decimal_places=2)
    tecnico = models.ForeignKey(Tecnico, on_delete=models.CASCADE, related_name='ventas_tecnico')
    cliente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ventas_cliente')  # Suponiendo que el cliente es un User
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Venta {self.id} - Publicación {self.publicacion.id} - Técnico {self.tecnico.user.username} - Cliente {self.cliente.username}"

    class Meta:
        verbose_name = 'Venta de Publicación'
        verbose_name_plural = 'Ventas de Publicaciones'

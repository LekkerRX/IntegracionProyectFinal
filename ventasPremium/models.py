from django.db import models
from django.contrib.auth.models import User  # Para asociar el pago con el técnico
from django.utils.timezone import now
from datetime import timedelta

class VentasPremium(models.Model):
    id = models.AutoField(primary_key=True)
    fecha = models.DateTimeField(default=now)
    cantidad_pago = models.DecimalField(max_digits=10, decimal_places=2)
    tecnico = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ventas_premium")
    fecha_caducidad = models.DateTimeField()

    def save(self, *args, **kwargs):
        # Calcular automáticamente la fecha de caducidad (un mes desde la fecha del pago)
        if not self.fecha_caducidad:
            self.fecha_caducidad = self.fecha + timedelta(days=30)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Venta Premium {self.id} - Técnico: {self.tecnico.username} - Monto: {self.cantidad_pago}"

from django.db import models
from django.contrib.auth.models import User
from Post.models import Publicacion

class Chat(models.Model):
    tecnico = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chats_como_tecnico')
    cliente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chats_como_cliente')
    publicacion = models.OneToOneField(Publicacion, on_delete=models.CASCADE, related_name='chat')
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat entre {self.cliente.username} y {self.tecnico.username} para {self.publicacion.titulo}"

class Mensaje(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='mensajes')
    remitente = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.TextField()
    adjunto = models.FileField(upload_to='mensajes_adjuntos/', null=True, blank=True)
    enviado_en = models.DateTimeField(auto_now_add=True)
    
    def remitente_nombre(self):
        return self.remitente.username

    def __str__(self):
        return f"Mensaje de {self.remitente.username} en {self.chat}"
    

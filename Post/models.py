
from django.db import models
from django.contrib.auth.models import User  # Importa el modelo User de Django
from multiselectfield import MultiSelectField
from Oficio.models import Oficio

class Publicacion(models.Model):
    # Título de la publicación
    visible_para_tecnicos = models.BooleanField(default=True)
    

    titulo = models.CharField(max_length=100, verbose_name="Título")

    # Descripción del problema técnico
    descripcion = models.TextField(verbose_name="Descripción")

    # Límite de monto a pagar
    limite_monto = models.PositiveIntegerField(verbose_name="Límite del monto a pagar (CLP)")

    # Imagen opcional
    imagen = models.ImageField(upload_to='publicaciones/', blank=True, null=True, verbose_name="Imagen del problema")

    # Ubicación
    ubicacion = models.CharField(max_length=255, verbose_name="Ubicación")

    # Relación con el modelo User (cliente) - cada publicación tiene un cliente asociado
    cliente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='publicaciones', verbose_name="Cliente")
    
    OFICIOS_CHOICES = [
        ('fontaneria', 'Técnico en fontanería'),
        ('electricidad', 'Técnico en electricidad'),
        ('climatizacion', 'Técnico en climatización'),
        ('carpinteria', 'Técnico en carpintería'),
        ('pintura', 'Técnico en pintura'),
        ('cerrajeria', 'Técnico en cerrajería'),
        ('electrodomesticos', 'Técnico en reparación de electrodomésticos'),
        ('seguridad', 'Técnico en instalación de sistemas de seguridad'),
        ('jardineria', 'Técnico en mantenimiento de jardines'),
        ('gas', 'Técnico en gas'),
        ('energias_renovables', 'Técnico en instalación de sistemas de energía renovable'),
        ('domotica', 'Técnico en sistemas de domótica'),
        ('dranaje', 'Técnico en drenaje y saneamiento'),
        ('impermeabilizacion', 'Técnico en impermeabilización'),
        ('piscinas', 'Técnico en mantenimiento de piscinas'),
        ('remodelacion', 'Técnico en remodelación de interiores'),
        ('reparacion_electrodomesticos_cocina', 'Técnico en reparación de electrodomésticos de cocina'),
        ('aislamiento', 'Técnico en aislamiento térmico y acústico'),
        ('telecomunicaciones', 'Técnico en instalación de sistemas de telecomunicaciones'),
        ('computadoras', 'Técnico en reparación de computadoras y dispositivos electrónicos'),
        ('limpieza', 'Técnico en limpieza profunda'),
        ('cortinas', 'Técnico en instalación de cortinas y persianas'),
        ('plagas', 'Técnico en exterminación de plagas'),
        ('tapiceria', 'Técnico en tapicería'),
        ('electrodomesticos_pequenos', 'Técnico en reparación de electrodomésticos pequeños'),
        ('agua_potable', 'Técnico en instalación de sistemas de agua potable'),
        ('instalaciones_sanitarias', 'Técnico en instalaciones sanitarias'),
        ('calefaccion', 'Técnico en instalación de sistemas de calefacción'),
        ('ventilacion', 'Técnico en instalación de sistemas de ventilación'),
        ('mantenimiento_telecomunicaciones', 'Técnico en mantenimiento de sistemas de telecomunicaciones y cableado'),
        ('alarma_incendios', 'Técnico en sistemas de alarma contra incendios'),
        ('techos', 'Técnico en reparación de techos y cubiertas'),
        ('paneles_solares_termicos', 'Técnico en instalaciones de paneles solares térmicos'),
        ('tratamiento_aguas_residuales', 'Técnico en instalación de sistemas de tratamiento de aguas residuales'),
        ('climatizacion_industrial', 'Técnico en mantenimiento de sistemas de climatización industrial'),
        ('otros', 'Otro'),
    ]
    oficios = models.ManyToManyField(Oficio, related_name='publicaciones', verbose_name="Oficios requeridos")

    
    fecha_publicacion = models.DateTimeField(auto_now=True)
    

    ESTADO_CHOICES = [
        ('esperando tecnico', 'Esperando Técnico'),
        ('tecnico atendiendo', 'Técnico Atendiendo Publicación'),
        ('publicacion atendida', 'Publicación Atendida'),
    ]
    
    estado = models.CharField(max_length=50, choices=ESTADO_CHOICES, default='esperando tecnico', verbose_name="Estado")
    
    def __str__(self):
        return self.titulo



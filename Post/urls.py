from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'Post' 

urlpatterns = [
    
    path('gestionar_publicaciones/', views.gestionar_publicaciones, name='gestionar_publicaciones'),
    path('eliminar_publicacion/<int:publicacion_id>/', views.eliminar_publicacion, name='eliminar_publicacion'),
    path('aceptar_tecnico/', views.aceptar_tecnico, name='aceptar_tecnico'),
    path('eliminar_tecnico/<int:publicacion_id>/<int:tecnico_id>/', views.eliminar_tecnico, name='eliminar_tecnico'),
    path('eliminar-notificacion/<int:notificacion_id>/', views.eliminar_notificacion_tecnico, name='eliminar_notificacion_tecnico'),
    
    



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
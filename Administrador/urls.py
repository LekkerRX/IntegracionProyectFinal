# urls.py
from django.urls import path
from . import views

app_name = 'Administrador' 

urlpatterns = [
    path('admin/credenciales/', views.lista_credenciales, name='lista_credenciales'),
    path('admin/credenciales/verificar/<int:credencial_id>/', views.verificar_credencial, name='verificar_credencial'),
    path('admin/credenciales/rechazar/<int:credencial_id>/', views.rechazar_credencial, name='rechazar_credencial'),
    path('admin/gestionar_publicaciones/', views.gestionar_publicaciones, name='gestionar_publicaciones'),
    path('notificacion/<int:notificacion_id>/marcar_como_leida/', views.marcar_como_leida_admin, name='marcar_como_leida_admin'),
    path('notificacion/<int:notificacion_id>/marcar_como_leida/', views.marcar_como_leida_tecnico, name='marcar_como_leida_tecnico'),
    path('notificacion/<int:notificacion_id>/marcar_como_leida/', views.marcar_como_leida_usuario, name='marcar_como_leida_usuario'),
    path('lista_perfiles/', views.lista_perfiles, name='lista_perfiles'),
    path('gestionar_perfil/<int:usuario_id>/', views.gestionar_perfil, name='gestionar_perfil'),
    path('panel/', views.panel_administrador, name='panel_administrador'),
    path('reseñas/', views.panel_administracion_reseñas, name='panel_administracion_reseñas'),
    path('reseñas/editar/<int:reseña_id>/', views.editar_reseña, name='editar_reseña'),
    path('reseñas/eliminar/<int:reseña_id>/', views.eliminar_reseña, name='eliminar_reseña'),
    path('reporte_ventas_premium/', views.reporte_ventas_premium, name='reporte_ventas_premium'),
    
]


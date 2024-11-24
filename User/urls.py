from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'User' 

urlpatterns = [
    
    path('', views.pagina_inicio, name='pagina_inicio'),
    path('register/', views.registro_tecnico, name='register'),
    path('registerClient/', views.client_register, name='register_client'),
    path('login/', views.custom_login, name='login'),
    path('loginClient/', views.client_login_client, name='login_client'),
    path('tecnico/', views.pagina_tecnico, name='pagina_tecnico'),

    path('perfil/', views.perfil_tecnico, name='perfil_tecnico'),
    path('logout/', views.custom_logout, name='logout'),  # URL de logout
    path('publicaciones-tecnico/', views.publicaciones_tecnico, name='publicaciones_tecnico'),
    path('postular/<int:publicacion_id>/', views.postular_publicacion, name='postular_publicacion'),
    path('perfil/tecnico/<int:id>/', views.perfil_tecnico_cliente, name='perfil_tecnico_cliente'),
    path('toggle-favorito/<int:publicacion_id>/', views.toggle_favorito, name='toggle_favorito'),

    
    
    
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
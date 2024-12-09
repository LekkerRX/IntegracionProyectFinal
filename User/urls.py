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
    path('confirmar-pago/', views.confirmar_pago, name='confirmar_pago'),
    path('perfil/', views.perfil_tecnico, name='perfil_tecnico'),
    path('logout/', views.custom_logout, name='logout'),  # URL de logout
    path('publicaciones-tecnico/', views.publicaciones_tecnico, name='publicaciones_tecnico'),
    path('postular/<int:publicacion_id>/', views.postular_publicacion, name='postular_publicacion'),
    path('perfil/tecnico/<int:id>/', views.perfil_tecnico_cliente, name='perfil_tecnico_cliente'),
    path('toggle-favorito/<int:publicacion_id>/', views.toggle_favorito, name='toggle_favorito'),
    path('crear-preferencia/<int:tecnico_id>/<int:publicacion_id>/<int:chat_id>/', views.crear_preferencia, name='crear_preferencia'),
    path('confirmar-pago/', views.confirmar_pago, name='confirmar_pago'),
    path('confirmar-pago-premium/', views.confirmar_pago_premium, name='confirmar_pago_premium'),
    path('premium/', views.premium, name='premium'),
    path('dejar_resena/<int:tecnico_id>/', views.dejar_resena, name='dejar_resena'),
    path('guardar_reseña/', views.guardar_reseña, name='guardar_reseña'),
    path('ranking/', views.ranking_tecnicos, name='ranking_tecnicos'),
    path('confirmar-pago-failure/', views.confirmar_pago_failure, name='confirmar_pago_failure'),
    path('confirmar-pago-failure-publicacion/', views.confirmar_pago_failure_publicacion, name='confirmar_pago_failure_publicacion'),




    
    
    
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
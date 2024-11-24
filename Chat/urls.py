from django.urls import path
from . import views

app_name = 'Chat'

urlpatterns = [

    path('<int:chat_id>', views.detalle_chat, name='detalle_chat'),
    path('mis-chats/<int:chat_id>/', views.detalle_chat_tecnico, name='detalle_chat_tecnico'),  # Aquí se recibe chat_id
]

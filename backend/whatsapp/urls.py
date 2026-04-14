from django.urls import path
from .views import send_whatsapp_client

urlpatterns = [

    path(
        'send/<int:client_id>/',
        send_whatsapp_client,
        name='send_whatsapp_client'
    ),

]
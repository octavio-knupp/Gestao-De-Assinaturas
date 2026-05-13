from django.urls import path

from .views import (
    send_whatsapp_client,
    toggle_whatsapp_automation,
    get_whatsapp_automation_status
)

urlpatterns = [

    path(
        'send/<int:client_id>/',
        send_whatsapp_client,
        name='send_whatsapp_client'
    ),

    path(
        'toggle-whatsapp-automation/',
        toggle_whatsapp_automation,
        name='toggle_whatsapp_automation'
    ),

    path(
        'get-whatsapp-automation-status/',
        get_whatsapp_automation_status,
        name='get_whatsapp_automation_status'
    ),
]
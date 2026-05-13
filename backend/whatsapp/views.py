from django.shortcuts import (
    get_object_or_404,
    redirect
)

from django.contrib.auth.decorators import login_required

from django.http import JsonResponse

from django.views.decorators.http import require_POST

import json

from clients.models import Client

from .models import WhatsAppAutomation

from .services import (
    get_status_and_message,
    send_whatsapp_message
)


# =====================================
# ENVIO MANUAL WHATSAPP
# =====================================

@login_required
def send_whatsapp_client(request, client_id):

    client = get_object_or_404(
        Client,
        id=client_id,
        owner=request.user
    )

    status, message = get_status_and_message(client)

    if message:

        send_whatsapp_message(
            client.phone,
            message
        )

    return redirect('list_clients')


# =====================================
# TOGGLE AUTOMAÇÃO
# =====================================

@require_POST
def toggle_whatsapp_automation(request):

    data = json.loads(request.body)

    active = data.get("active", False)

    automation, created = (
        WhatsAppAutomation.objects.get_or_create(
            id=1
        )
    )

    automation.active = active

    automation.save()

    print("AUTOMAÇÃO:", automation.active)

    return JsonResponse({
        "success": True,
        "active": automation.active
    })


# =====================================
# STATUS AUTOMAÇÃO
# =====================================

def get_whatsapp_automation_status(request):

    automation = WhatsAppAutomation.objects.first()

    active = False

    if automation:
        active = automation.active

    return JsonResponse({
        "active": active
    })
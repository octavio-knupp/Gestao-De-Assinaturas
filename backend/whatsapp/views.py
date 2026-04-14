from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from clients.models import Client
from .services import (
    get_status_and_message,
    send_whatsapp_message
)


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
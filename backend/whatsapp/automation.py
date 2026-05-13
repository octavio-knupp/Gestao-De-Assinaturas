import threading
import time

from datetime import date

from clients.models import Client

from .models import WhatsAppAutomation

from .services import (
    get_status_and_message,
    send_whatsapp_message
)


def start_whatsapp_automation():

    def run():

        while True:

            try:

                print("VERIFICANDO AUTOMAÇÃO...")

                automation = WhatsAppAutomation.objects.first()

                if automation and automation.active:

                    print("AUTOMAÇÃO ATIVA")

                    clients = Client.objects.all()

                    print(
                        f"{clients.count()} clientes encontrados"
                    )

                    for client in clients:

                        status, message = get_status_and_message(
                            client
                        )

                        print(
                            f"{client.first_name} -> {status}"
                        )

                        # só envia:
                        # vencido
                        # vence hoje
                        # vence breve
                        if not message:

                            print(
                                "Cliente em dia. Ignorado."
                            )

                            continue

                        # já enviou hoje?
                        if client.last_whatsapp_sent == date.today():

                            print(
                                f"{client.first_name} já recebeu hoje"
                            )

                            continue

                        print(
                            f"Enviando para {client.first_name}"
                        )

                        send_whatsapp_message(
                            client.phone,
                            message
                        )

                        client.last_whatsapp_sent = date.today()

                        client.save()

                        print(
                            f"Mensagem enviada para {client.first_name}"
                        )

                        # evita conflito no pywhatkit
                        time.sleep(40)

                else:

                    print(
                        "AUTOMAÇÃO DESATIVADA"
                    )

                # TESTE
                time.sleep(10)

            except Exception as e:

                print(
                    "Erro automação WhatsApp:",
                    e
                )

                time.sleep(60)

    thread = threading.Thread(
        target=run,
        daemon=True
    )

    thread.start()

    
import pywhatkit as kit
import datetime
import time
import pyautogui

from datetime import date, timedelta


def get_status_and_message(client):

    today = date.today()

    if client.due_date < today:

        status = "vencido"

        message = (
            f"Olá {client.first_name},\n\n"
            f"Sua assinatura está vencida.\n\n"
            f"Regularize o pagamento para reativar o serviço."
        )

    elif client.due_date == today:

        status = "vence_hoje"

        message = (
            f"Olá {client.first_name},\n\n"
            f"Sua assinatura vence hoje.\n\n"
            f"Evite a suspensão e renove agora."
        )

    elif client.due_date <= today + timedelta(days=3):

        status = "vence_breve"

        message = (
            f"Olá {client.first_name},\n\n"
            f"Sua assinatura irá vencer em breve.\n\n"
            f"Renove antecipadamente para evitar interrupções."
        )

    else:

        status = "em_dia"
        message = None

    return status, message


def send_whatsapp_message(phone, message):

    if not phone or not message:
        return

    phone = phone.strip()

    if not phone.startswith("+"):
        phone = "+55" + phone

    try:

        now = datetime.datetime.now()

        send_time = now + datetime.timedelta(minutes=1)

        hour = send_time.hour
        minute = send_time.minute

        kit.sendwhatmsg(
            phone,
            message,
            hour,
            minute,
            wait_time=25,
            tab_close=False
        )

        # Espera carregar o WhatsApp
        time.sleep(35)

        # Força envio
        pyautogui.press("enter")

    except Exception as e:

        print("Erro ao enviar WhatsApp:", e)
import pywhatkit as kit
import datetime
import time
import pyautogui

from datetime import date, timedelta


# =====================================
# STATUS + MENSAGEM
# =====================================

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


# =====================================
# ENVIO WHATSAPP
# =====================================

def send_whatsapp_message(phone, message):

    if not phone or not message:
        return

    phone = phone.strip()

    # adiciona +55 automaticamente
    if not phone.startswith("+55"):

        phone = "+55" + phone

    try:

        now = datetime.datetime.now()

        # tempo para abrir WhatsApp
        send_time = now + datetime.timedelta(minutes=2)

        hour = send_time.hour
        minute = send_time.minute

        print(f"Abrindo WhatsApp para {phone}")

        kit.sendwhatmsg(

            phone,
            message,

            hour,
            minute,

            wait_time=40,

            tab_close=False
        )

        # espera WhatsApp carregar totalmente
        time.sleep(20)

        print("Tentando enviar ENTER...")

        # garante foco na janela
        pyautogui.click()

        time.sleep(2)

        # envia mensagem
        pyautogui.press("enter")

        print(f"Mensagem enviada para {phone}")

    except Exception as e:

        print(
            "Erro ao enviar WhatsApp:",
            e
        )
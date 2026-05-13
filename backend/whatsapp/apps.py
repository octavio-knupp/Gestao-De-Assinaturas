import os

from django.apps import AppConfig


class WhatsappConfig(AppConfig):

    default_auto_field = 'django.db.models.BigAutoField'

    name = 'whatsapp'

    def ready(self):

        if os.environ.get('RUN_MAIN') != 'true':
            return

        print("AUTOMAÇÃO WHATSAPP INICIADA")

        from .automation import (
            start_whatsapp_automation
        )

        start_whatsapp_automation()
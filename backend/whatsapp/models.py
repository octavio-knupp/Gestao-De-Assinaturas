from django.db import models


class WhatsAppAutomation(models.Model):

    active = models.BooleanField(default=False)

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):

        return f"Automação ativa: {self.active}"
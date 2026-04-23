from django.db import models
from django.contrib.auth.models import User

class Client(models.Model):

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    first_name = models.CharField(
        max_length=100
    )

    last_name = models.CharField(
        max_length=100
    )

    phone = models.CharField(
        max_length=20
    )

    # DATA DE VENCIMENTO
    due_date = models.DateField()

    # MENSALIDADE
    monthly_fee = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0
    )

    # GÊNERO COM OPÇÕES FIXAS
    gender = models.CharField(
        max_length=1,
        choices=[
            ('M', 'Masculino'),
            ('F', 'Feminino'),
            ('O', 'Outro')

        ]
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.first_name
from django.db import models
from clients.models import Client
from plans.models import Plan

class Subscription(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)

    start_date = models.DateField()
    next_due_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=[
            ('active', 'Active'),
            ('canceled', 'Canceled'),
            ('pending', 'Pending'),
        ],
        default='active'
    )

    def __str__(self):
        return f"{self.client} - {self.plan}"
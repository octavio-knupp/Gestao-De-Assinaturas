from django.db import models
from django.contrib.auth.models import User
from plans.models import Plan

class Subscription(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    plan = models.ForeignKey(
        Plan,
        on_delete=models.CASCADE
    )

    start_date = models.DateField(
        auto_now_add=True
    )

    next_due_date = models.DateField(
        null=True,
        blank=True
    )

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
        return f"{self.user} - {self.plan}"
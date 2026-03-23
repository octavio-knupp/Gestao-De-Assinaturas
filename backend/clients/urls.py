from django.urls import path
from .views import create_client

urlpatterns = [
    path('', create_client, name='create_client'),
]
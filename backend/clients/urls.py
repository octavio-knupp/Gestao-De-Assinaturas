from django.urls import path
from .views import create_client, login_client

urlpatterns = [
    path('', create_client, name='create_client'),
    path('login/', login_client, name='login_client'),
]
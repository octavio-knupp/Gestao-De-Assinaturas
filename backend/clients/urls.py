from django.urls import path
from .views import create_client, login_client, home_client, logout_client

urlpatterns = [
    path('', home_client, name='home_client'),   # 👈 HOME na raiz
    path('login/', login_client, name='login_client'),
    path('create/', create_client, name='create_client'),
    path('logout/', logout_client, name='logout_client'),
]

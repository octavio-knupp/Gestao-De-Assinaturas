from django.urls import path

from .views import (
    create_client,
    login_client,
    home_client,
    logout_client,

    # CRUD CLIENTES
    list_clients,
    cadastro_client,
    update_client,
    delete_client
)

urlpatterns = [

    # HOME
    path(
        '',
        home_client,
        name='home_client'
    ),

    # AUTH
    path(
        'login/',
        login_client,
        name='login_client'
    ),

    path(
        'create/',
        create_client,
        name='create_client'
    ),

    path(
        'logout/',
        logout_client,
        name='logout_client'
    ),

    # CLIENTES (CRUD)

    path(
        'clients/',
        list_clients,
        name='list_clients'
    ),

    path(
    'clients/cadastro/',
    cadastro_client,
    name='cadastro_client'
    ),

    path(
        'clients/update/<int:client_id>/',
        update_client,
        name='update_client'
    ),

    path(
        'clients/delete/<int:client_id>/',
        delete_client,
        name='delete_client'
    ),

]
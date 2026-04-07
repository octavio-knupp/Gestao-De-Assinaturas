from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# 🚀 CADASTRO DE USUÁRIO
def create_client(request):
    if request.method == 'POST':

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        erros = []

        # 🔥 VALIDAÇÕES
        if password != confirm_password:
            erros.append('As senhas não coincidem!')

        if len(password) < 6:
            erros.append('A senha deve ter pelo menos 6 caracteres!')

        if User.objects.filter(username=email).exists():
            erros.append('Este email já está cadastrado!')

        if "@" not in email:
            erros.append('Email inválido!')

        # ❌ SE TIVER ERROS
        if erros:
            return render(request, 'create_client.html', {
                'erros': erros,
                'dados': request.POST
            })

        # ✅ CRIA USUÁRIO
        User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        return redirect('login_client')

    return render(request, 'create_client.html')


# 🔐 LOGIN
def login_client(request):
    if request.method == 'POST':

        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=email,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('home_client')
        else:
            return render(request, 'login_client.html', {
                'erro': 'Email ou senha inválidos'
            })

    return render(request, 'login_client.html')


# 🏠 HOME
@login_required
def home_client(request):
    return render(request, 'home_client.html', {
        'name': request.user.first_name
    })


# 🚪 LOGOUT
def logout_client(request):
    logout(request)
    return redirect('login_client')


# ===============================
# 📋 STATUS CLIENTE (LISTAGEM)
# ===============================

@login_required
def list_clients(request):

    return render(
        request,
        'list_client.html'
    )

# ===============================
# 📋 CADASTRO CLIENTE 
# ===============================

@login_required
def cadastro_client(request):

    return render(
        request,
        'cadastro_client.html'
    )


# ===============================
# ✏️ ALTERAÇÃO CLIENTE
# ===============================

@login_required
def update_client(request, client_id):

    return render(
        request,
        'update_client.html',
        {
            'client_id': client_id
        }
    )


# ===============================
# 🗑️ EXCLUSÃO CLIENTE
# ===============================

@login_required
def delete_client(request, client_id):

    return render(
        request,
        'delete_client.html',
        {
            'client_id': client_id
        }
    )


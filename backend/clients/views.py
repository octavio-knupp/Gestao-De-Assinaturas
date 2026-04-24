from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Client

from datetime import date, timedelta
from decimal import Decimal

from subscriptions.models import Subscription
from plans.models import Plan


# ===============================
# 🚀 CADASTRO DE USUÁRIO
# ===============================

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
            return render(
                request,
                'create_client.html',
                {
                    'erros': erros,
                    'dados': request.POST
                }
            )

        # ✅ CRIA USUÁRIO

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        # 🧠 CRIA ASSINATURA AUTOMÁTICA (BRONZE)

        plan = Plan.objects.get(name="Bronze")

        Subscription.objects.create(
            user=user,
            plan=plan,
            next_due_date=date.today() + timedelta(days=30)
        )

        return redirect('login_client')

    return render(request, 'create_client.html')


# ===============================
# 🔐 LOGIN
# ===============================

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

            return render(
                request,
                'login_client.html',
                {
                    'erro': 'Email ou senha inválidos'
                }
            )

    return render(request, 'login_client.html')


# ===============================
# 🏠 HOME
# ===============================

@login_required
def home_client(request):

    subscription = Subscription.objects.filter(
        user=request.user
    ).first()

    total_clients = Client.objects.filter(
        owner=request.user
    ).count()

    percentage = 0
    max_clients = None

    if subscription:

        plan = subscription.plan
        max_clients = plan.max_clients

        if max_clients:

            percentage = int(
                (total_clients / max_clients) * 100
            )

            if percentage > 100:
                percentage = 100

    return render(
        request,
        'home_client.html',
        {
            'subscription': subscription,
            'total_clients': total_clients,
            'max_clients': max_clients,
            'percentage': percentage
        }
    )


# ===============================
# 🚪 LOGOUT
# ===============================

def logout_client(request):

    logout(request)

    return redirect('login_client')


# ===============================
# 📋 STATUS CLIENTE (LISTAGEM)
# ===============================

@login_required
def list_clients(request):

    clients = Client.objects.filter(
        owner=request.user
    )

    today = date.today()

    clients_status = []

    for client in clients:

        if client.due_date < today:

            status = "vencido"

        elif client.due_date == today:

            status = "vence_hoje"

        elif client.due_date <= today + timedelta(days=3):

            status = "vence_breve"

        else:

            status = "em_dia"

        clients_status.append({

            'client': client,
            'status': status

        })

    return render(

        request,

        'list_client.html',

        {
            'clients_status': clients_status
        }

    )


# ===============================
# 📋 CADASTRO CLIENTE
# ===============================

@login_required
def cadastro_client(request):

    if request.method == 'POST':

        # 🔎 BUSCA ASSINATURA

        subscription = Subscription.objects.filter(
            user=request.user
        ).first()

        if not subscription:

            return render(
                request,
                'cadastro_client.html',
                {
                    'erro': 'Usuário sem assinatura ativa.'
                }
            )

        plan = subscription.plan

        # 🔎 CONTAR CLIENTES

        total_clients = Client.objects.filter(
            owner=request.user
        ).count()

        # 🚫 VERIFICAR LIMITE

        if plan.max_clients is not None:

            if total_clients >= plan.max_clients:

                return render(
                    request,
                    'cadastro_client.html',
                    {
                        'erro': 'Limite de clientes atingido para seu plano.'
                    }
                )

        # 💰 TRATAR MENSALIDADE

        monthly_fee_value = request.POST.get('monthly_fee')

        if not monthly_fee_value:
            monthly_fee_value = 0

        monthly_fee = Decimal(monthly_fee_value)

        # ✅ CRIAR CLIENTE

        Client.objects.create(

            owner=request.user,

            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            phone=request.POST.get('phone'),
            gender=request.POST.get('gender'),
            due_date=request.POST.get('due_date'),
            monthly_fee=monthly_fee

        )

        return redirect('cadastro_client')

    return render(
        request,
        'cadastro_client.html'
    )


# ===============================
# ✏️ ALTERAÇÃO CLIENTE
# ===============================

@login_required
def update_client(request, client_id):

    client = get_object_or_404(
        Client,
        id=client_id,
        owner=request.user
    )

    if request.method == 'POST':

        client.first_name = request.POST.get('first_name')
        client.last_name = request.POST.get('last_name')
        client.phone = request.POST.get('phone')
        client.gender = request.POST.get('gender')
        client.due_date = request.POST.get('due_date')

        monthly_fee_value = request.POST.get('monthly_fee')

        if not monthly_fee_value:
            monthly_fee_value = 0

        client.monthly_fee = Decimal(monthly_fee_value)

        client.save()

        return redirect('list_clients')

    return render(
        request,
        'update_client.html',
        {
            'client': client
        }
    )


# ===============================
# 🗑️ EXCLUSÃO CLIENTE
# ===============================

@login_required
def delete_client(request, client_id):

    client = get_object_or_404(
        Client,
        id=client_id,
        owner=request.user
    )

    if request.method == 'POST':

        client.delete()

        return redirect('list_clients')

    return render(
        request,
        'delete_client.html',
        {
            'client': client
        }
    )
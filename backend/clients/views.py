from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from django.db.models import Sum

from .models import Client, UserProfile

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
        phone = request.POST.get('phone') or request.POST.get('telefone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        erros = []

        if password != confirm_password:
            erros.append('As senhas não coincidem!')

        if len(password) < 6:
            erros.append('A senha deve ter pelo menos 6 caracteres!')

        if User.objects.filter(username=email).exists():
            erros.append('Este email já está cadastrado!')

        if "@" not in email:
            erros.append('Email inválido!')

        if erros:
            return render(
                request,
                'create_client.html',
                {
                    'erros': erros,
                    'dados': request.POST
                }
            )

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        UserProfile.objects.create(
            user=user,
            phone=phone
        )

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

            return redirect('dashboard_client')

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
# 📊 DASHBOARD
# ===============================

@login_required
def dashboard_client(request):

    today = date.today()
    breve = today + timedelta(days=3)

    clients = Client.objects.filter(
        owner=request.user
    )

    total_clients = clients.count()

    clients_vencidos = clients.filter(
        due_date__lt=today
    ).count()

    clients_vence_hoje = clients.filter(
        due_date=today
    ).count()

    clients_vence_breve = clients.filter(
        due_date__gt=today,
        due_date__lte=breve
    ).count()

    clients_em_dia = clients.filter(
        due_date__gt=breve
    ).count()

    faturamento_mensal = clients.aggregate(
        total=Sum('monthly_fee')
    )['total'] or Decimal('0.00')

    valor_vencido = clients.filter(
        due_date__lt=today
    ).aggregate(
        total=Sum('monthly_fee')
    )['total'] or Decimal('0.00')

    subscription = Subscription.objects.filter(
        user=request.user
    ).first()

    plan = None
    max_clients = None
    percentage = 0

    if subscription:

        plan = subscription.plan
        max_clients = plan.max_clients

        if max_clients:

            percentage = int(
                (total_clients / max_clients) * 100
            )

            if percentage > 100:
                percentage = 100

    ultimos_clientes = clients.order_by(
        '-created_at'
    )[:5]

    proximos_vencimentos = clients.filter(
        due_date__gte=today
    ).order_by(
        'due_date'
    )[:5]

    return render(
        request,
        'dashboard_client.html',
        {
            'total_clients': total_clients,
            'clients_em_dia': clients_em_dia,
            'clients_vencidos': clients_vencidos,
            'clients_vence_hoje': clients_vence_hoje,
            'clients_vence_breve': clients_vence_breve,
            'faturamento_mensal': faturamento_mensal,
            'valor_vencido': valor_vencido,
            'subscription': subscription,
            'plan': plan,
            'max_clients': max_clients,
            'percentage': percentage,
            'ultimos_clientes': ultimos_clientes,
            'proximos_vencimentos': proximos_vencimentos,
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

    pesquisa = request.GET.get('pesquisa', '').strip()
    status_filter = request.GET.get('status', 'todos')

    clients = Client.objects.filter(
        owner=request.user
    ).order_by('id')

    if pesquisa:

        clients = clients.filter(
            Q(first_name__icontains=pesquisa) |
            Q(last_name__icontains=pesquisa) |
            Q(phone__icontains=pesquisa)
        )

    today = date.today()
    breve = today + timedelta(days=3)

    if status_filter == 'todos' or not status_filter:
        pass

    elif status_filter == 'vencido':

        clients = clients.filter(
            due_date__lt=today
        )

    elif status_filter == 'vence_hoje':

        clients = clients.filter(
            due_date=today
        )

    elif status_filter == 'vence_breve':

        clients = clients.filter(
            due_date__gt=today,
            due_date__lte=breve
        )

    elif status_filter == 'em_dia':

        clients = clients.filter(
            due_date__gt=breve
        )

    clients_status = []

    for client in clients:

        if client.due_date < today:
            status = "vencido"

        elif client.due_date == today:
            status = "vence_hoje"

        elif client.due_date <= breve:
            status = "vence_breve"

        else:
            status = "em_dia"

        clients_status.append({
            'client': client,
            'status': status
        })

    paginator = Paginator(clients_status, 15)
    page_number = request.GET.get('page')
    clients_status = paginator.get_page(page_number)

    return render(
        request,
        'list_client.html',
        {
            'clients_status': clients_status,
            'status_selected': status_filter,
            'pesquisa': pesquisa
        }
    )


# ===============================
# 📋 CADASTRO CLIENTE
# ===============================

@login_required
def cadastro_client(request):

    if request.method == 'POST':

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

        total_clients = Client.objects.filter(
            owner=request.user
        ).count()

        if plan.max_clients is not None:

            if total_clients >= plan.max_clients:

                return render(
                    request,
                    'cadastro_client.html',
                    {
                        'erro': 'Limite de clientes atingido para seu plano.'
                    }
                )

        monthly_fee_value = request.POST.get('monthly_fee')

        if not monthly_fee_value:
            monthly_fee_value = 0

        monthly_fee = Decimal(monthly_fee_value)

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


# ===============================
# ⚙️ CONFIGURAÇÕES
# ===============================

@login_required
def config_client(request):

    subscription = Subscription.objects.filter(
        user=request.user
    ).first()

    total_clients = Client.objects.filter(
        owner=request.user
    ).count()

    plan = None
    max_clients = None
    percentage = 0
    phone = "Não informado"
    status_active = False

    if hasattr(request.user, 'profile') and request.user.profile.phone:
        phone = request.user.profile.phone

    if subscription:

        plan = subscription.plan
        max_clients = plan.max_clients

        status = str(subscription.status).strip().lower()
        status_active = status in ['ativo', 'active']

        if max_clients:

            percentage = int(
                (total_clients / max_clients) * 100
            )

            if percentage > 100:
                percentage = 100

    return render(
        request,
        'config.html',
        {
            'subscription': subscription,
            'plan': plan,
            'phone': phone,
            'status_active': status_active,
            'clientes_cadastrados': total_clients,
            'total_clients': total_clients,
            'max_clients': max_clients,
            'percentage': percentage,
            'uso_percentual': percentage
        }
    )
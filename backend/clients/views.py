from django.shortcuts import render, redirect
from .models import Client

def create_client(request):
    if request.method == 'POST':

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        gender = request.POST.get('gender')

        erros = []

        # 🔥 VALIDAÇÕES

        # Senha
        if password != confirm_password:
            erros.append('As senhas não coincidem!')

        if len(password) < 6:
            erros.append('A senha deve ter pelo menos 6 caracteres!')

        # Email duplicado
        if Client.objects.filter(email=email).exists():
            erros.append('Este email já está cadastrado!')

        # Email inválido (simples)
        if "@" not in email:
            erros.append('Email inválido!')

        # Telefone (simples)
        if not phone.isdigit():
            erros.append('Telefone deve conter apenas números!')

        if len(phone) < 10:
            erros.append('Telefone inválido!')

        # ❌ SE TIVER ERRO → NÃO SALVA
        if erros:
            return render(request, 'create_client.html', {
                'erros': erros,
                'dados': request.POST
            })

        # ✅ SALVA
        Client.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            password=password,
            gender=gender
        )

        return redirect('create_client')

    return render(request, 'create_client.html')

def login_client(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            client = Client.objects.get(email=email, password=password)
            return redirect('create_client')  # depois você muda isso
        except Client.DoesNotExist:
            return render(request, 'login_client.html', {
                'erro': 'Email ou senha inválidos'
            })

    return render(request, 'login_client.html')
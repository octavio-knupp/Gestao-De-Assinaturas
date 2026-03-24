from django.shortcuts import render, redirect
from .models import Client

def create_client(request):
    if request.method == 'POST':
        print("CHEGOU POST")

        try:
            Client.objects.create(
                first_name=request.POST.get('first_name'),
                last_name=request.POST.get('last_name'),
                email=request.POST.get('email'),
                phone=request.POST.get('phone'),
                password=request.POST.get('password'),
                gender=request.POST.get('gender')
            )
            print("SALVOU NO BANCO")

            return redirect('create_client')

        except Exception as e:
            print("ERRO:", e)

            return render(request, 'create_client.html', {
                'error': str(e)
            })

    return render(request, 'create_client.html')
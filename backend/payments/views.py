import stripe
from datetime import date, timedelta

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from plans.models import Plan
from subscriptions.models import Subscription
from payments.models import Payment


stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def pagamentos(request):
    return render(request, 'pagamentos.html', {
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY
    })


@login_required
def create_checkout_session(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método inválido'}, status=405)

    plan_name = request.POST.get('plan')

    if not plan_name:
        return JsonResponse({'error': 'Plano não informado'}, status=400)

    plan = Plan.objects.filter(name__iexact=plan_name).first()

    if not plan:
        return JsonResponse({'error': 'Plano não encontrado'}, status=404)

    subscription, created = Subscription.objects.get_or_create(
        user=request.user,
        defaults={
            'plan': plan,
            'status': 'pending',
            'next_due_date': date.today() + timedelta(days=30)
        }
    )

    if not created:
        subscription.plan = plan
        subscription.status = 'pending'
        subscription.next_due_date = date.today() + timedelta(days=30)
        subscription.save()

    success_url = request.build_absolute_uri(
        reverse('payment_success')
    ) + '?session_id={CHECKOUT_SESSION_ID}'

    cancel_url = request.build_absolute_uri(
        reverse('payment_cancel')
    )

    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        mode='payment',
        line_items=[
            {
                'price_data': {
                    'currency': 'brl',
                    'product_data': {
                        'name': f'Plano {plan.name}',
                    },
                    'unit_amount': int(plan.price * 100),
                },
                'quantity': 1,
            }
        ],
        metadata={
            'user_id': request.user.id,
            'plan_id': plan.id,
            'subscription_id': subscription.id,
        },
        success_url=success_url,
        cancel_url=cancel_url,
    )

    Payment.objects.create(
        subscription=subscription,
        amount=plan.price,
        status='pending',
        stripe_checkout_session_id=checkout_session.id,
        payment_method='stripe'
    )

    return redirect(checkout_session.url)


@login_required
def payment_success(request):
    session_id = request.GET.get('session_id')

    if session_id:
        session = stripe.checkout.Session.retrieve(session_id)

        if session.payment_status == 'paid':
            payment = Payment.objects.filter(
                stripe_checkout_session_id=session_id
            ).first()

            if payment:
                payment.status = 'paid'
                payment.stripe_payment_intent_id = session.payment_intent
                payment.save()

                subscription = payment.subscription
                subscription.status = 'active'
                subscription.next_due_date = date.today() + timedelta(days=30)
                subscription.save()

    return render(request, 'payment_success.html')


@login_required
def payment_cancel(request):
    return render(request, 'payment_cancel.html')
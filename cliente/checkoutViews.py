# views.py
from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings
from main.models import Carrito_Detalle
from paypal.standard.forms import PayPalPaymentsForm
import uuid

def CheckOut(request):
    # Obtener los productos del carrito
    if request.user.is_authenticated:
        qsCarrito = Carrito_Detalle.objects.filter(user_id=request.user)
    else:
        qsCarrito = Carrito_Detalle.objects.filter(session_key=request.session.session_key)

    # Calcular el total y configurar los elementos del carrito para PayPal
    total = 0
    for item in qsCarrito:
        total += item.producto_id.precio * item.unidades

    item_name = "Compra en mi tienda"  # Nombre del artículo que aparecerá en PayPal

    host = request.get_host()

    # Configurar el formulario de PayPal
    paypal_checkout = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': str(total),
        'item_name': item_name,
        'invoice': str(uuid.uuid4()),
        'currency_code': 'USD',
        'notify_url': f"http://{host}{reverse('paypal-ipn')}",
        'return_url': f"http://{host}{reverse('cliente:payment-success')}",
        'cancel_url': f"http://{host}{reverse('cliente:payment-failed')}",
    }

    paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)

    context = {
        'qsCarrito': qsCarrito,
        'paypal': paypal_payment
    }

    return render(request, 'cliente/checkout.html', context)

    
# views.py (continuación)
def PaymentSuccessful(request):
    if request.user.is_authenticated:
        Carrito_Detalle.objects.filter(user_id=request.user).delete()
    else:
        Carrito_Detalle.objects.filter(session_key=request.session.session_key).delete()

    return render(request, 'cliente/payment-success.html')

def PaymentFailed(request):
    return render(request, 'cliente/payment-failed.html')

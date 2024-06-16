from decimal import Decimal
import json
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import FormView, TemplateView
from django.views import View
from django import forms
from django import db
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
# Create your views here.f
from cliente.funciones import generateAccessToken, create_order, capture_order
from main.models import Pedido_cabecera, Pedido_detalle, Producto
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes



class HomeView(TemplateView):
    template_name = 'index.html'


class PayForm(forms.Form):
    count = forms.IntegerField()
    
    
class PayView(FormView):
    template_name = 'pay.html'
    form_class = PayForm
    success_url = '/'
    
    def form_valid(self, form):
        print(form.cleaned_data['count'])
        #
        print('----')
        respuesta = generateAccessToken()
        print(respuesta)
        return super().form_valid(form)


class CrearOrden(APIView):    
    def post(self,  request, *args, **kwargs):
        try:           
            carrito = request.data.get('cart', [])
            order = create_order(carrito)
            print('=====')
            print(order['id'])
            return Response(order, status=status.HTTP_200_OK)
        except Exception as err:
            print(err)
            return err


class CapturarOdernPaypal(APIView):
    
    def post(self, request, *args, **kwargs):
        try:
            order_id = request.data.get('orderID')  # Obtener orderID desde la solicitud            
            carrito = request.session.get('carrito', {}) 
            try:
                carrito = json.loads(carrito) if isinstance(carrito, str) else carrito
            except json.JSONDecodeError:
                carrito = {}
            # Realizar la captura de la orden en PayPal
            response = capture_order(order_id)
            
            if response['status'] == 'COMPLETED':
                # Procesar cada elemento del carrito y guardar en la base de datos
                productos_comprados = []
                with db.transaction.atomic():
                    pedido_cabecera = Pedido_cabecera(
                            usuario_id=request.user,   
                            order_id=order_id,                     
                        )
                    pedido_cabecera.save()
                    for key, detalles in carrito.items():
                        producto = Producto.objects.get(id=key)
                        unidades = detalles['unidades']                   
                        # Guardar cada producto comprado en la base de datos
                    
                        pedido_detalle = Pedido_detalle(
                            nombre=producto.nombre,
                            producto_id=producto,
                            precio=producto.precio,
                            unidades=unidades, 
                            porcentaje=producto.porcentaje,
                            iva=producto.iva,                                               
                            pedido_cabecera_id=pedido_cabecera,
                        )

                        pedido_detalle.save()
                        producto.unidades = producto.unidades - unidades
                        producto.save                    
                        productos_comprados.append(pedido_detalle)
                        # Vaciar el carrito después de una compra exitosa
                        request.session['carrito'] = {}     
                        request.session["add_contexto"]=dict(
                        toast=dict(
                            titulo='Pago',
                            tipo='success',
                            mensaje="El pago si ha realizado correctamente"
                            )         
                        )

                    return Response({
                        'status': 'COMPLETED',
                        'redirect_url': reverse('cliente:mostrar_carrito'),
                        'id_pedido_cabecera':pedido_cabecera.id,
                    }, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'El pago no se completó correctamente'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            print(error)
            return Response({'error': 'Ocurrió un error al procesar el pago'}, status=status.HTTP_400_BAD_REQUEST)
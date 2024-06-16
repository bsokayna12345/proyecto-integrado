from decimal import Decimal
import json
from django.shortcuts import redirect, render
from django.views.generic import FormView, TemplateView
from django.views import View
from django import forms
#
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


# class CapturarOdernPaypal(APIView):
    
#     def post(self, request, *args, **kwargs):
#         try:
#             order_id = self.kwargs['order_id']
#              # Obtener el carrito de la solicitud POST
#             cart = request.data.get('cart')
            
#             # Realizar la captura de la orden en PayPal
#             response = capture_order(order_id)
            
#             # Aquí puedes hacer algo con el carrito, por ejemplo, guardarlo en la base de datos
            
#             return Response(response, status=status.HTTP_200_OK)
#         except Exception as error:
#             print(error)
#             return Response({'error': 'error aquí'}, status=status.HTTP_400_BAD_REQUEST)
@method_decorator(login_required(login_url='administracion:login'), name='dispatch')
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
                for key, detalles in carrito.items():
                    producto = Producto.objects.get(id=key)
                    unidades = detalles['unidades']
                    precio = Decimal(detalles['precio'])
                    precio_oferta = Decimal(detalles['precio_oferta']) if detalles['precio_oferta'] != 'None' else None
                    total = precio_oferta * unidades if precio_oferta else precio * unidades
                    # Guardar cada producto comprado en la base de datos
                    pedido_cabecera = Pedido_cabecera(
                        usuario_id=request.user,                        
                    )
                    pedido_cabecera.save()
                    pedido_detalle = Pedido_detalle(
                        nombre=producto.nombre,
                        producto=producto,
                        precio=total,
                        unidades=unidades,                        
                        # order_id=order_id,  # Guardar el ID de la orden de PayPal para referencia
                        pedido_cabecera_id=pedido_cabecera
                    )

                    pedido_detalle.save()
                    producto.unidades = producto.unidades - unidades
                    producto.save                    
                    productos_comprados.append(pedido_detalle)
                
                context = {
                    'mensaje': 'Pago realizado correctamente',
                    'productos_comprados': productos_comprados
                }
                return render(request, 'pago-hecho.html', context)
            else:
                return Response({'error': 'El pago no se completó correctamente'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            print(error)
            return Response({'error': 'Ocurrió un error al procesar el pago'}, status=status.HTTP_400_BAD_REQUEST)
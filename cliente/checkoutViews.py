from decimal import Decimal
import json
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import FormView, TemplateView
from django.views import View
from django import forms
from django import db
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# Create your views here.f
from cliente.funciones import generateAccessToken, create_order, capture_order
from main.models import Pedido_cabecera, Pedido_detalle, Producto
from django.core.mail import send_mail



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
                        # usuario_email = 'irmatica871.'
                        # asunto = 'Gracias por tu compra'
                        # mensaje = 'Tu compra ha sido realizada con éxito. ¡Gracias por comprar con nosotros!'
                        # remitente = settings.EMAIL_HOST_USER
                        # destinatario = [usuario_email]

                        # # Enviar el correo electrónico
                        # send_mail(asunto, mensaje, remitente, destinatario)


                    # return Response({
                    #     'status': 'COMPLETED',
                    #     'redirect_url': reverse('cliente:detalles_carrito'),
                    #     'id_pedido_cabecera': pedido_cabecera.id,
                        
                    # }, status=status.HTTP_200_OK)
                    return Response({
                        'status': 'COMPLETED',                        
                        'id_pedido_cabecera': pedido_cabecera.id,
                    }, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'El pago no se completó correctamente'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            print(error)
            return Response({'error': 'Ocurrió un error al procesar el pago'}, status=status.HTTP_400_BAD_REQUEST)
        

class DetallesCompra(TemplateView):
    template_name = "cliente/detalles_compra.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obtener el ID del pedido de los parámetros de la URL
        pedido_id = self.kwargs.get('order_id')
        
        # Obtener la cabecera del pedido desde la base de datos
        pedido_cabecera = get_object_or_404(Pedido_cabecera, id=pedido_id)
        
        # Obtener los detalles del pedido utilizando el related_name 'detalles'
        qsPedido_detalle = pedido_cabecera.detalles.all()
        if qsPedido_detalle is not None:
            total_precio = 0
            for producto_id in qsPedido_detalle:
                producto_id.imagen_p= producto_id.producto_id.get_Producto_ImagenProducto.filter(imagen_principal=True).first() 
                precio = producto_id.precio  # Precio del producto
                iva = producto_id.iva                       
                precio_con_iva = Decimal(str(precio)) * (Decimal('1') + Decimal(str(iva)))     
                producto_id.precio_con_iva = precio_con_iva                 
                # si tengo producto de oferta  
                if producto_id.producto_id.en_oferta == True:                                            
                    porcentaje = producto_id.porcentaje
                    porcentaje_oferta = Decimal(str(porcentaje)) / Decimal('100')
                    precio_oferta = precio_con_iva  * (Decimal('1') - porcentaje_oferta)                                          
                    producto_id.precio_oferta = precio_oferta   
                    total_precio += precio_oferta
                else:
                    # Sumar el precio con IVA al total
                    total_precio += precio_con_iva  
        # Pasar la cabecera y los detalles del pedido al contexto de la plantilla
        context = dict(
            pedido_cabecera=pedido_cabecera,
            qsPedido_detalle=qsPedido_detalle,
            total_precio=total_precio,
        )
      
        
        return context

        
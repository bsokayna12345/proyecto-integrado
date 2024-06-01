import json
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic.base import TemplateView
from main.funciones import  desencriptar, encriptar
from django.http import HttpResponseServerError
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from main.models import Carrito_Detalle, Producto, SubCategoria


# Create your views here.
from django.shortcuts import render

class ProductoListPageView(TemplateView):
    """ lista de producto  """
    template_name='cliente/inicio.html'

    def contexto(self, request, qsProducto:Producto): #form:formulariofilter
        try:
            toast=dict(
                titulo='desde el ninici toast titulo',
                tipo='success'
            )
            contador_unidades_carrito = 0
            qsCarrito = Carrito_Detalle.objects.filter(user_id=request.user)
            if qsCarrito.count() > 0 :
                for carrito_id in qsCarrito:
                    contador_unidades_carrito = contador_unidades_carrito + carrito_id.unidades                
            contexto = dict(
                qsProducto=qsProducto,
                toast=toast, 
                contador_unidades_carrito=contador_unidades_carrito,                              
            )
            return contexto
        except Exception as Err:
            return Err
     
    def get(self, request, *args, **kwargs):
        qsProducto = Producto.objects.all()
        contexto = self.contexto(request, qsProducto)
        return render(request, self.template_name, contexto)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class ProductoDetalle(TemplateView):
    """ detalle de un producto """
    template_name='cliente/producto-detalle.html'

    def contexto(self, request, producto_id:Producto): #form:formulariofilter
        try:
            contador_unidades_carrito = 0
            qsCarrito = Carrito_Detalle.objects.filter(user_id=request.user)
            if qsCarrito.count() > 0 :
                for carrito_id in qsCarrito:
                    contador_unidades_carrito = contador_unidades_carrito + carrito_id.unidades 
            contexto = dict(
                producto_id=producto_id,
                contador_unidades_carrito=contador_unidades_carrito,
            )
            return contexto
        except Exception as Err:
            return Err
     
    def get(self, request, *args, **kwargs):
        key = kwargs.get('key', None)
        producto_id = Producto.objects.get(id=key)
        contexto = self.contexto(request, producto_id)
        return render(request, self.template_name, contexto)    

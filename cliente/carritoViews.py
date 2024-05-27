import json
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic.base import TemplateView
from main.funciones import  desencriptar, encriptar
from django.http import HttpResponseServerError
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from main.models import Producto, SubCategoria


# Create your views here.
from django.shortcuts import render

class CarritoListPageViews(TemplateView):
    """ lista de carrito  """
    template_name='cliente/carrito-list.html'

    def contexto(self, request, qsProducto:Producto):
        try:
            contexto = dict(
                qsProducto=qsProducto,
            )
            return contexto
        except Exception as Err:
            return Err
     
    def get(self, request, *args, **kwargs):
        try:                
            key = kwargs.get("key", None)
            if key is None:
                contexto =self.context(request=request,producto_id=None, unidades=0)              
            return render(request, self.template_name, contexto)
        except Exception as Err:
            return Err
            
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

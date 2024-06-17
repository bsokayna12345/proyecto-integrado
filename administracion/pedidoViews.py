from decimal import Decimal
import json
from django import db
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic.base import TemplateView
from administracion.permisos import class_view_decorator, superuser_required
from main.funciones import  desencriptar, encriptar
from django.http import HttpResponseServerError
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from main.models import Pedido_cabecera, Pedido_detalle

# Create your views here.

@class_view_decorator(superuser_required)
class PedidoListFilterPageView(TemplateView):
    """ lista de producto  """
    template_name='administracion/pedidos-list.html'

    def contexto(self, request, qsProducto:Pedido_cabecera): #form:formulariofilter
        try:                                                         
            contexto = dict(
                qsProducto=qsProducto,
            )
            return contexto
        except Exception as Err:
            return Err
     
    def get(self, request, *args, **kwargs):        
        qsProducto = Pedido_cabecera.objects.all()
        contexto = self.contexto(request, qsProducto)
        if request.session.get("add_contexto", None) is not None:
            contexto.update(request.session["add_contexto"])
            del request.session["add_contexto"]
        return render(request, self.template_name, contexto)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
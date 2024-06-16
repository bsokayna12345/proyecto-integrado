import json
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic.base import TemplateView
from main.funciones import  desencriptar, encriptar
from django.http import HttpResponseServerError
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from main.models import  Producto, SubCategoria


# Create your views here.
from django.shortcuts import render

class ProductoOfertaListPageView(TemplateView):
    """ lista de productos de oferta  """
    template_name='cliente/ofertas.html'

    def contexto(self, request, qsProducto:Producto): #form:formulariofilter
        try:
                       
            for producto_id in qsProducto:
                producto_id.imagen_p= producto_id.get_Producto_ImagenProducto.filter(imagen_principal=True).first()
                
            contexto = dict(
                qsProducto=qsProducto,                                                                                         
                previous_url = request.META.get('HTTP_REFERER')
            )
            return contexto
        except Exception as Err:
            mensaje = Err.args[0]
            request.session["add_contexto"]=dict(
                toast=dict(
                    titulo='Error',
                    tipo='Error',
                    mensaje=mensaje                    
                    )         
                )  
            return {}
     
    def get(self, request, *args, **kwargs):
        key_categoria = kwargs.get('key_categoria', None)
        qsProducto=None
        if key_categoria is not None:
            subcategoria_id = SubCategoria.objects.filter(categoria_id__id=key_categoria).first()
            qsProducto = Producto.objects.filter(subcategoria_id=subcategoria_id, en_oferta=True)
        else:
            qsProducto = Producto.objects.filter(en_oferta=True)
        contexto = self.contexto(request = request, qsProducto = qsProducto)
        if request.session.get("add_contexto", None) is not None:
            contexto.update(request.session["add_contexto"])
            del request.session["add_contexto"]
        return render(request, self.template_name, contexto)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
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
            
            contador_unidades_carrito = 0   

            if request.user.is_authenticated:
                qsCarrito = Carrito_Detalle.objects.filter(user_id=request.user)
            else:
                qsCarrito = Carrito_Detalle.objects.filter(session_key=request.session.session_key)                                 
            if qsCarrito.count() > 0 :
                for carrito_id in qsCarrito:
                    contador_unidades_carrito = contador_unidades_carrito + carrito_id.unidades                
            #anadir las imagenes principal al producto
            for producto_id in qsProducto:
                producto_id.imagen_p= producto_id.get_Producto_ImagenProducto.filter(imagen_principal=True).first()
            contexto = dict(
                qsProducto=qsProducto,                                 
                contador_unidades_carrito=contador_unidades_carrito,                                         
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
            qsProducto = Producto.objects.filter(subcategoria_id=subcategoria_id)
        else:
            qsProducto = Producto.objects.all()
        contexto = self.contexto(request = request, qsProducto = qsProducto)
        if request.session.get("add_contexto", None) is not None:
            contexto.update(request.session["add_contexto"])
            del request.session["add_contexto"]
        return render(request, self.template_name, contexto)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class ProductoDetalle(TemplateView):
    """ detalle de un producto """
    template_name='cliente/producto-detalle.html'

    def contexto(self, request, producto_id:Producto): #form:formulariofilter
        try:
            contador_unidades_carrito = 0
            if request.user.is_authenticated:
                qsCarrito = Carrito_Detalle.objects.filter(user_id=request.user)
            else:
                qsCarrito = Carrito_Detalle.objects.filter(session_key=request.session.session_key)
                if qsCarrito.count() > 0 :
                    for carrito_id in qsCarrito:
                        contador_unidades_carrito = contador_unidades_carrito + carrito_id.unidades 
            producto_id.imagen_p =  producto_id.get_Producto_ImagenProducto.filter(imagen_principal=True).first()
            producto_id.imagenes =  producto_id.get_Producto_ImagenProducto.all()
            contexto = dict(
                producto_id=producto_id,
                contador_unidades_carrito=contador_unidades_carrito,
            )
            return contexto
        except Exception as Err:
            print(Err)
            return {}
     
    def get(self, request, *args, **kwargs):
        try:
            key = kwargs.get('key', None)
            producto_id = Producto.objects.get(id=key)
            contexto = self.contexto(request, producto_id)
            if request.session.get("add_contexto", None) is not None:
                contexto.update(request.session["add_contexto"])
                del request.session["add_contexto"]        
            return render(request, self.template_name, contexto)  
        except Exception as Err:
            mensaje = Err.args[0]
            request.session["add_contexto"]=dict(
                toast=dict(
                    titulo='Error',
                    tipo='Error',
                    mensaje=mensaje                    
                    )         
                )  
            return redirect(reverse('cliente:producto_list'))

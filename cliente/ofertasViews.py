import json
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic.base import TemplateView
from django.db.models import Q
from main.models import  Categoria, Producto, SubCategoria


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
                categorias = Categoria.objects.all().prefetch_related('get_Categoria_SubCategoria'),

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
        key_subcategoria = kwargs.get('key_subcategoria', None)
        qsProducto=None
        if key_subcategoria is not None:
            subcategoria_id = SubCategoria.objects.filter(id=key_subcategoria).first()
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
    

class ProductoOfertaBuscarListPageView(TemplateView):
    """ detalle de un producto """
    template_name='cliente/ofertas.html'

    def contexto(self, request, qsProducto:Producto): #form:formulariofilter
        try:        

            for producto_id in qsProducto:
                producto_id.imagen_p= producto_id.get_Producto_ImagenProducto.filter(imagen_principal=True).first()
            contexto = dict(
                qsProducto=qsProducto,     
                categorias = Categoria.objects.all().prefetch_related('get_Categoria_SubCategoria'),
                                                                                              
            )
            return contexto
        except Exception as Err:
            print(Err)
            return {}
     
    def get(self, request, *args, **kwargs):
        try:
            filtro =  request.GET.get('buscar', None)        
            qsProducto = Producto.objects.filter(en_oferta=True)
            if filtro:
                qsProducto = qsProducto.filter(
                    Q(nombre__icontains=filtro) |
                    Q(subcategoria_id__categoria_id__nombre__icontains=filtro) |
                    Q(marca_id__nombre__icontains=filtro) |
                    Q(subcategoria_id__nombre__icontains=filtro)
                )
            contexto = self.contexto(request, qsProducto)
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
            return redirect(reverse('cliente:oferta_list'))
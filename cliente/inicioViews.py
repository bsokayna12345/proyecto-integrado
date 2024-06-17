import json
from django import db
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic.base import TemplateView
from cliente.comentarioForms import ComentarioForm
from main.funciones import  desencriptar, encriptar
from django.http import HttpResponseServerError
from django.db.models import Q
from main.models import  Categoria, Pedido_detalle, Producto, SubCategoria


# Create your views here.
from django.shortcuts import render

class ProductoListPageView(TemplateView):
    """ lista de producto  """
    template_name='cliente/inicio.html'

    def contexto(self, request, qsProducto:Producto): #form:formulariofilter
        try:            
                                                                                                                
            #anadir las imagenes principal al producto
            for producto_id in qsProducto:
                producto_id.imagen_p= producto_id.get_Producto_ImagenProducto.filter(imagen_principal=True).first()                
            contexto = dict(
                categorias = Categoria.objects.all().prefetch_related('get_Categoria_SubCategoria'),
                qsProducto=qsProducto,                    
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
        comando = kwargs.get("comando", None)
        qsProducto=None
        if key_subcategoria is not None:
            subcategoria_id = SubCategoria.objects.filter(id=key_subcategoria).first()
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

            pedido_detalle = Pedido_detalle.objects.filter(producto_id=producto_id, pedido_cabecera_id__usuario_id=request.user)  
            producto_id.imagen_p =  producto_id.get_Producto_ImagenProducto.filter(imagen_principal=True).first()
            producto_id.imagenes =  producto_id.get_Producto_ImagenProducto.all()
            contexto = dict(
                producto_id=producto_id,     
                form_comentario = ComentarioForm(),
                comentarios = producto_id.get_Comentario_Producto.all(),    
                pedido_detalle = pedido_detalle,
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
    def post(self, request, *args, **kwargs):
        try:      
            key_producto = kwargs.get('key', None)
            producto_id = Producto.objects.get(id=key_producto)            
            form_comentario = ComentarioForm(request.POST)
            # 
            pedido_detalle = Pedido_detalle.objects.filter(producto_id=producto_id, pedido_cabecera_id__usuario_id=request.user)
            if pedido_detalle is not None:
                with db.transaction.atomic():
                    if form_comentario.is_valid():
                        comentario = form_comentario.save(commit=False)
                        comentario.producto_id = producto_id
                        comentario.usuario_id = request.user
                        comentario.save()                                   
                        return redirect(reverse('cliente:producto_detalle', kwargs=dict(key=key_producto)))                        
        except Exception as Err:
            #request.session["add_contexto"]["toast"]["mensaje"].args
            mensaje = Err.args[0]
            request.session["add_contexto"]=dict(
                toast=dict(
                    titulo='Error',
                    tipo='Error',
                    mensaje=mensaje                    
                    )         
                )
            return redirect(reverse('cliente:producto_list')) 

class ProductoBuscarListPageView(TemplateView):
    """ detalle de un producto """
    template_name='cliente/inicio.html'

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
            qsProducto = Producto.objects.all()
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
            return redirect(reverse('cliente:producto_list'))
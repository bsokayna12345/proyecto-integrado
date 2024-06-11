import json
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic.base import TemplateView

from django.http import HttpResponseServerError
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from main.models import Categoria, ImagenProducto, Producto, SubCategoria
from administracion.productoForms import ImagenForm, ProductoForm

# Create your views here.
from django.shortcuts import render

class ProductoListFilterPageView(TemplateView):
    """ lista de producto  """
    template_name='administracion/producto-list.html'

    def contexto(self, request, qsProducto:Producto): #form:formulariofilter
        try:
            contexto = dict(
                qsProducto=qsProducto,
            )
            return contexto
        except Exception as Err:
            return Err
     
    def get(self, request, *args, **kwargs):
        qsProducto = Producto.objects.all()
        contexto = self.contexto(request, qsProducto)
        if request.session.get("add_contexto", None) is not None:
            contexto.update(request.session["add_contexto"])
            del request.session["add_contexto"]
        return render(request, self.template_name, contexto)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

@method_decorator(login_required(login_url='administracion:login'), name='dispatch')    
class ProductoEditPageView(TemplateView):
    """ editar o añadir producto """
    template_name ="administracion/producto-edit.html"
    def contexto(self, request,producto_id:Producto): 
        try:  
            key = None 
            form = ProductoForm()
            form_imagen = ImagenForm()
            secure_data = None
            qsImagenProducto = None
            if producto_id is not None:                       
                form = ProductoForm(instance=producto_id, initial=dict(
                    subcategoria_id =  SubCategoria.objects.filter(id=producto_id.subcategoria_id.id).first(),
                    categoria_id= Categoria.objects.filter(id=producto_id.subcategoria_id.categoria_id.id).first(),
                ))
                form.fields["subcategoria_id"].queryset = SubCategoria.objects.filter(id=producto_id.subcategoria_id.id) 
                form.fields["categoria_id"].queryset = Categoria.objects.filter(id=producto_id.subcategoria_id.categoria_id.id)    
                
                qsImagenProducto =  producto_id.get_Producto_ImagenProducto.all()
                key = producto_id.id    
                                        
            contexto = dict(
                form=form,               
                secure_data=secure_data,
                form_imagen=form_imagen,
                qsImagenProducto=qsImagenProducto,
            )           
            return contexto
        except Exception as Err:
            return Err
     
    def get(self, request, *args, **kwargs):
        contexto = dict()
        try:   
            key = kwargs.get('key', None)            
            if key is not None:   
                producto_id = Producto.objects.get(id=key)
            else:
                producto_id = None                                                   
            contexto = self.contexto(request, producto_id=producto_id)       
            if request.session.get("add_contexto", None) is not None:
                contexto.update(request.session["add_contexto"])
                del request.session["add_contexto"]
         
            return render(request, self.template_name, contexto)
        except Exception as Err:
            return Err          

    def post(self, request, *args, **kwargs):
        try:    
            key = kwargs.get('key')                                                               
            if key is not None:                                                      
                producto_id = Producto.objects.filter(id=key).first() 
                form = ProductoForm(request.POST, instance=producto_id)
                form.fields["subcategoria_id"].queryset = SubCategoria.objects.filter(id=request.POST.get("subcategoria_id"))
                key = key             
            else:
                form = ProductoForm(request.POST)                 
                form.fields["subcategoria_id"].queryset = SubCategoria.objects.filter(id=request.POST.get("subcategoria_id"))   
                
            comando = request.POST.get('comando', None)            
            if comando == 'guardar':
                if form.is_valid():
                    form.save()
                    titulo='Guardar'
                    tipo='success'
                    mensaje='Los datos se han guardado correctamente'
                else:
                    titulo='Guardar'
                    tipo='Error'
                    mensaje='Los datos No se han guardado'
                    raise ValueError("El formulario no es válido")
                request.session["add_contexto"]=dict(
                    toast=dict(
                        titulo=titulo,
                        tipo=tipo,
                        mensaje=mensaje,
                    ) 
               )
            
            if comando == 'eliminar':               
                producto_id.delete() 
                mensaje='Se ha eleminado el producto'
                request.session["add_contexto"]=dict(
                toast=dict(
                    titulo='Eliminar',
                    tipo='Info',
                    mensaje='Se ha eleminado el producto'
            )    )
                return redirect(reverse('administracion:producto_list')) 
           
            return redirect(reverse('administracion:producto_edit', kwargs=dict(key=form.instance.id)))        
            
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
            return redirect(reverse('administracion:producto_list')) 

class SubirImagen(TemplateView):

    def post(self, request, *args, **kwargs):
        try:               
            key_producto = kwargs.get('key_producto')                                                    
            if key_producto is not None:                     
                producto_id = Producto.objects.filter(id=key_producto).first() 
                form_imagen = ImagenForm(request.POST, request.FILES)    
                if form_imagen.is_valid():                            
                    ImagenProducto(
                        producto_id=producto_id,
                        imagen=form_imagen.cleaned_data['imagen']
                    ).save()
                    request.session["add_contexto"]=dict(
                    toast=dict(
                        titulo="Guardar",
                        tipo="success",
                        mensaje='Los datos se han guardado correctamente',
                    ) 
               )                               
            return redirect(reverse('administracion:producto_edit', kwargs=dict(key=key_producto)))        
            
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
            return redirect(reverse('administracion:producto_list')) 
import json
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic.base import TemplateView
from main.funciones import  desencriptar, encriptar
from django.http import HttpResponseServerError
from main.models import Producto, SubCategoria
from .productoForms import ProductoForm

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
        return render(request, self.template_name, contexto)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
        
class ProductoEditPageView(TemplateView):
    """ editar o añadir producto """
    template_name ="administracion/producto-edit.html"
    def contexto(self, request,producto_id:Producto): 
        try:  
            key = None 
            form = ProductoForm()
            secure_data = None
            if producto_id is not None:                       
                form = ProductoForm(instance=producto_id)
                form.fields["subcategoria_id"].queryset = SubCategoria.objects.filter(id=producto_id.subcategoria_id.id) 
                
                key = producto_id.id    
                secure_data=encriptar(dict(key=str(key)))         
            contexto = dict(
                form=form,
                secure_data=secure_data
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
         
            return render(request, self.template_name, contexto)
        except Exception as Err:
            return Err       
   


    def post(self, request, *args, **kwargs):
        try:    
            key = kwargs.get('key')                                           
            secure_data = request.POST.get("secure_data", None)          
            if secure_data not in ["None"]:                            
                dict_desencriptado = desencriptar(secure_data, {"key":str(key)})             
                if dict_desencriptado:                              
                    producto_id = Producto.objects.filter(id=key).first() 
                    form = ProductoForm(request.POST, instance=producto_id)
                    form.fields["subcategoria_id"].queryset = SubCategoria.objects.filter(id=request.POST.get("subcategoria_id"))
                    key = key
                else :
                    raise NameError("los datos están corruptos")
            else:
                form = ProductoForm(request.POST) 
                form.fields["subcategoria_id"].queryset = SubCategoria.objects.filter(id=request.POST.get("subcategoria_id"))                        
            comando = request.POST.get('comando', None)            
            if comando == 'guardar':
                if form.is_valid():
                    form.save()
                else:
                    raise ValueError("El formulario no es válido")
            if comando == 'eliminar':               
                producto_id.delete()
                return redirect(reverse('administracion:producto_list'))   
            return redirect(reverse('administracion:producto_edit', kwargs=dict(key=form.instance.id)))        
            
        except Exception as Err:
            return Err




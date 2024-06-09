import json
from django import db
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic.base import TemplateView
from main.funciones import  desencriptar, encriptar
from django.http import HttpResponseServerError
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from main.models import Carrito_Detalle, Producto, SubCategoria
from django.shortcuts import render
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid

    
class CarritoListPageView(TemplateView):
    """ ver el carrito"""
    template_name='cliente/carrito-list.html'

    def contexto(self, request, qsCarrito:Carrito_Detalle):
        """
        CONTEXTO
        """        
        try:
            contador_unidades_carrito = 0
            subtotal = 0
            if qsCarrito is not None:                           
                if qsCarrito.count() > 0 :
                    for producto_id in qsCarrito:
                        contador_unidades_carrito = contador_unidades_carrito + producto_id.unidades 
                        producto_id.precio_total = producto_id.producto_id.precio * producto_id.unidades
                        subtotal += producto_id.precio_total
                        producto_id.imagen_p = producto_id.producto_id.get_Producto_ImagenProducto.filter(imagen_principal=True).first()
           
            contexto = dict(
                qsCarrito=qsCarrito,
                contador_unidades_carrito=contador_unidades_carrito,
                subtotal=subtotal,
            )            
            return contexto
        
        except Exception as Err:
            print(Err)
            return 
        
    def get(self, request, *args, **kwargs):
        try:
            
            if request.user.is_authenticated:
                qsCarrito = Carrito_Detalle.objects.filter(user_id=request.user)
            else:
                qsCarrito = Carrito_Detalle.objects.filter(session_key=request.session.session_key)
               
            contexto = self.contexto(request=request, qsCarrito=qsCarrito)
            return render(request, self.template_name, contexto)
        except Exception as err:
            print(err)
            return redirect('cliente:producto_list')
    
    def post(self, request, *args, **kwargs):
        """ añadir al carrito o eliminar del carrito"""
        try:              
            key = kwargs.get('key', None)             # key de producto
            producto_id = Producto.objects.filter(id=key).first()
            comando = request.POST.get("comando")
           
            unidades_intoducida = request.POST.get('unidades', None)   
            # comprobar si hay sufisientes unidades
            if producto_id is None:
                raise NameError('No existe el producto')                       
            else:
                if producto_id.unidades < int(unidades_intoducida):
                    raise NameError('!insuficiente unidades¡')  
                if comando == "añadir":                                   
                    with db.transaction.atomic(): 
                        if request.user.is_authenticated:
                            carrito_id = Carrito_Detalle.objects.filter(user_id=request.user, producto_id=producto_id).first()
                        else:
                            carrito_id = Carrito_Detalle.objects.filter(session_key=request.session.session_key, producto_id=producto_id).first()                                                 
                        if carrito_id is not None:                            
                            # existe
                            carrito_id.unidades = carrito_id.unidades + 1 
                        else:                
                            # no existe el producto
                            carrito_id = Carrito_Detalle()
                            carrito_id.user_id=request.user
                            carrito_id.producto_id=producto_id
                            carrito_id.unidades=1
                        carrito_id.save()   
                        producto_id.unidades = producto_id.unidades - int(unidades_intoducida)# editar las unidades
                        producto_id.save()     
                    return redirect(reverse('cliente:producto_list', kwargs=dict(key=key)))                
                if comando == "modificar":
                    if request.user.is_authenticated:
                        carrito_id = Carrito_Detalle.objects.filter(user_id=request.user, producto_id=producto_id).first()
                    else:
                        carrito_id = Carrito_Detalle.objects.filter(session_key=request.session.session_key, producto_id=producto_id).first()                    
                    carrito_id.unidades = int(unidades_intoducida)
                    carrito_id.save()
                    producto_id.unidades = producto_id.unidades - int(unidades_intoducida )
                    producto_id.save()
                
                if comando == "eliminar":
                    if request.user.is_authenticated:
                        carrito_id = Carrito_Detalle.objects.filter(user_id=request.user, producto_id=producto_id).first()
                    else:
                        carrito_id = Carrito_Detalle.objects.filter(session_key=request.session.session_key, producto_id=producto_id).first()
                    if carrito_id is not None:
                        carrito_id.delete()                                            
                return redirect('cliente:carrito_list')
        except Exception as err:
            print(err)
            return redirect('cliente:producto_list')      
                
def anadirAlCarrito(request, key):    
    try:
        if request.method == "POST":                
            producto_id = Producto.objects.filter(id=key).first()
            unidades_intoducida = request.POST.get('unidades', None)   
            # comprobar si hay sufisientes unidades
            if producto_id is None:
                raise NameError('!insuficiente unidades¡')                       
            else:
                if producto_id.unidades < int(unidades_intoducida):
                    raise NameError('!insuficiente unidades¡')                                     
                with db.transaction.atomic():        
                    if request.user.is_authenticated:                  
                        carrito_id = Carrito_Detalle.objects.filter(user_id=request.user, producto_id=producto_id).first()# buscar en el carrito si existe el producto
                    else:
                        carrito_id = Carrito_Detalle.objects.filter(session_key=request.session.session_key, producto_id=producto_id).first()# buscar en el carrito si existe el producto
                    if carrito_id is not None:
                        # existe
                        carrito_id.unidades = carrito_id.unidades + 1 
                    else:                
                        # no existe el producto
                        carrito_id = Carrito_Detalle()
                        carrito_id.user_id=request.user
                        carrito_id.session_key=request.session.session_key
                        carrito_id.producto_id=producto_id
                        carrito_id.unidades=1
                    carrito_id.save()   
                    producto_id.unidades = producto_id.unidades - int(unidades_intoducida)# editar las unidades
                    producto_id.save()     
                return redirect(reverse('cliente:producto_detalle', kwargs=dict(key=key)))
    except Exception as err:
            print(err)
            return redirect('cliente:producto_list')      
            
        

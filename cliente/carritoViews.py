import json
from django import db
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic.base import TemplateView
from cliente.funciones import generateAccessToken
from cliente.inicioViews import ProductoDetalle
from main.funciones import  desencriptar, encriptar
from django.http import HttpResponseServerError
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from main.models import Carrito_Detalle, Producto, SubCategoria
from django.shortcuts import render
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid

    

class addirAlcarrito(TemplateView):
    """ añadir producto a la cesta """
    def post(self, request, *args, **kwargs):
        try:
            #request.session.flush()
            titulo = ""
            tipo = ""
            mensaje = ""
            key = kwargs.get('key_producto', None)            
            unidades = int(request.POST.get("unidades"))
            carrito = request.session.get('carrito', {})            
            # Obtener el producto de la base de datos
            producto = get_object_or_404(Producto, id=key)
            try:
                carrito = json.loads(carrito) if isinstance(carrito, str) else carrito
            except json.JSONDecodeError:
                carrito = {}
            # Hacer una comprobación de unidades
            if unidades > producto.unidades:                              
                titulo="Añadir producto a la cesta"
                tipo="Info"
                mensaje='¡No hay suficientes unidades!'                                          
            else:
                # Verificar si el producto ya está en el carrito
                if str(key) in carrito:
                    carrito[str(key)]['unidades'] += unidades                
                else:
                    carrito[str(key)] = {
                        'nombre': producto.nombre,
                        'precio': str(producto.precio),  # Almacena como cadena para JSON
                        'precio_oferta': None if str(producto.precio_oferta) is None else   str(producto.precio_oferta),
                        'unidades': unidades,
                        'imagen': producto.get_Producto_ImagenProducto.first().imagen.url if producto.get_Producto_ImagenProducto.first() else ""
                    }
               
                titulo="Añadir producto a la cesta"
                tipo="success"
                mensaje='Si ha añadido correctamento'
              
            request.session["add_contexto"]=dict(
                toast=dict(
                    titulo=titulo,
                    tipo=tipo,
                    mensaje=mensaje
                    )         
                )            
            # Actualizar la sesión            
            request.session['carrito'] = json.dumps(carrito) 
            return redirect(reverse('cliente:producto_detalle', kwargs=dict(key=key)))
        except Exception as err:
            mensaje = err.args[0]
            request.session["add_contexto"]=dict(
                toast=dict(
                    titulo='Error',
                    tipo='Error',
                    mensaje=mensaje
                    )         
                )
            return redirect('cliente:producto_list')
class MostrarCarrito(TemplateView):    
    """Ver el carrito"""
    template_name = 'cliente/carrito-list.html'

    def get(self, request, *args, **kwargs):
        carrito = request.session.get('carrito', {})
        
        # Si el carrito está guardado como una cadena JSON, lo deserializamos
        if isinstance(carrito, str):          
            carrito = json.loads(carrito)
        
        total_carrito = 0  # Inicializa el subtotal del carrito
        items_a_remover = []  # Lista de items a remover si no existen

        # Calcular el precio total por producto y el subtotal del carrito
        for item_id, item in list(carrito.items()):  # Convertimos a lista para modificar el diccionario mientras iteramos
            try:
                producto = Producto.objects.get(id=item_id)
                # comprovar si el producto es de oferta 
                if producto.en_oferta == True:
                    item['precio_total'] = None if  item['precio_oferta'] is None else float(item['precio_oferta']) * item['unidades']
                else:

                    item['precio_total'] = float(item['precio']) * item['unidades']
                item['id'] = producto.id
                total_carrito += item['precio_total']
            except Producto.DoesNotExist:                
                items_a_remover.append(item_id)
        
        # Remover productos no existentes del carrito
        for item_id in items_a_remover:
            del carrito[item_id]
        
        # Actualizar la sesión si hubo cambios
        if items_a_remover:
            request.session['carrito'] = carrito
        #carrito item list para realizar el pago
        cart_items = []
        precio_total = 0
        subtotal = 0

        for item_id, item in list(carrito.items()):
            producto = Producto.objects.get(id=item_id)
            if producto.en_oferta:
                precio_total = float(item['precio_oferta']) * item['unidades']
            else:
                precio_total = float(item['precio']) * item['unidades']
            subtotal += precio_total            
            precio_decimal = producto.precio
            precio_float = float(precio_decimal)
            cart_items.append({
                'id': producto.id,
                'name': producto.nombre,
                'quantity': item['unidades'],
                'price': precio_float,
            })
            cart_items.append(dict(subtotal=float(subtotal)))
        return render(request, self.template_name, {'carrito': carrito, 'total_carrito': total_carrito, 'cart_items':json.dumps(cart_items)})

class ModificarCarrito(TemplateView):
    """ añadir producto a la cesta """

    def post(self, request, *args, **kwargs):
        try:
            titulo = ""
            tipo = ""
            mensaje = ""
            key = kwargs.get('key_producto', None)           
            unidades = int(request.POST.get("unidades"))
            carrito = request.session.get('carrito', {})            
            # Obtener el producto de la base de datos
            producto = get_object_or_404(Producto, id=key)
            try:
                carrito = json.loads(carrito) if isinstance(carrito, str) else carrito
            except json.JSONDecodeError:
                carrito = {}
            # Hacer una comprobación de unidades
            comando = request.POST.get('comando', None)
            if comando == "modificar":
                if unidades > producto.unidades:                              
                    titulo="Añadir producto a la cesta"
                    tipo="Info"
                    mensaje='¡No hay suficientes unidades!'                                            
                else:  
                    carrito[str(key)]['unidades'] = unidades 
            if comando == "eliminar":
                del carrito[str(key)]
                titulo="Añadir producto a la cesta"
                tipo="Info"
                mensaje='¡Producto eliminado!'  
            
            request.session['carrito'] = carrito

            request.session["add_contexto"]=dict(
                toast=dict(
                    titulo=titulo,
                    tipo=tipo,
                    mensaje=mensaje
                    )         
                )
            return redirect('cliente:mostrar_carrito')  
        
        except Exception as err:
            mensaje = err.args[0]
            request.session["add_contexto"]=dict(
                toast=dict(
                    titulo='Error',
                    tipo='Error',
                    mensaje=mensaje
                    )         
                )
            return redirect('cliente:mostrar_carrito')

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
            cart_items = []
            if qsCarrito is not None:                           
                if qsCarrito.count() > 0 :
                    for producto_id in qsCarrito:
                        contador_unidades_carrito = contador_unidades_carrito + producto_id.unidades 
                        producto_id.precio_total = producto_id.producto_id.precio * producto_id.unidades
                        subtotal += producto_id.precio_total
                        producto_id.imagen_p = producto_id.producto_id.get_Producto_ImagenProducto.filter(imagen_principal=True).first()
                        precio_decimal = producto_id.producto_id.precio
                        precio_float = float(precio_decimal)
                        cart_items.append({
                            'id': producto_id.id,
                            'name': producto_id.producto_id.nombre,
                            'quantity': producto_id.unidades,
                            'price': precio_float,
                        })
                    cart_items.append(dict(subtotal=float(subtotal))) 
            contexto = dict(
                qsCarrito=qsCarrito,
                contador_unidades_carrito=contador_unidades_carrito,
                cart_items=json.dumps(cart_items),
                subtotal=subtotal,
                respuesta = generateAccessToken()
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
        try:
            
            if request.user.is_authenticated:
                qsCarrito = Carrito_Detalle.objects.filter(user_id=request.user)
            else:
                qsCarrito = Carrito_Detalle.objects.filter(session_key=request.session.session_key)            
            contexto = self.contexto(request=request, qsCarrito=qsCarrito)
            if request.session.get("add_contexto", None) is not None:
                contexto.update(request.session["add_contexto"])
                del request.session["add_contexto"]
            return render(request, self.template_name, contexto)
        except Exception as err:
            mensaje = err.args[0]
            request.session["add_contexto"]=dict(
                toast=dict(
                    titulo='Error',
                    tipo='Error',
                    mensaje=mensaje
                    )         
                )
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
                if comando == "añadir":      
                    if producto_id.unidades < int(unidades_intoducida):
                        raise NameError('!insuficiente unidades¡')                               
                    with db.transaction.atomic(): 
                        if request.user.is_authenticated:
                            carrito_id = Carrito_Detalle.objects.filter(user_id=request.user, producto_id=producto_id).first()
                            if carrito_id is not None:                            
                                # existe
                                carrito_id.unidades = carrito_id.unidades + 1 
                            else:                
                                # no existe el producto
                                carrito_id = Carrito_Detalle()   
                                carrito_id.user_id=request.user                         
                                carrito_id.producto_id=producto_id
                                carrito_id.unidades=1
                        else:
                            carrito_id = Carrito_Detalle.objects.filter(session_key=request.session.session_key, producto_id=producto_id).first()                                                 
                            if carrito_id is not None:                            
                                # existe
                                carrito_id.unidades = carrito_id.unidades + 1 
                            else:                
                                # no existe el producto
                                carrito_id = Carrito_Detalle()    
                                carrito_id.session_key= request.session.session_key                       
                                carrito_id.producto_id=producto_id
                                carrito_id.unidades=1
                        carrito_id.save()   
                        producto_id.unidades = producto_id.unidades - int(unidades_intoducida)# editar las unidades
                        producto_id.save()
                        request.session["add_contexto"]=dict(
                        toast=dict(
                            titulo="Guardar",
                            tipo="success",
                            mensaje='Los datos se han guardado correctamente',
                        ) 
                    )
                    return redirect(reverse('cliente:producto_list'))                
                if comando == "modificar":
                    if request.user.is_authenticated:
                        carrito_id = Carrito_Detalle.objects.filter(user_id=request.user, producto_id=producto_id).first()
                    else:
                        carrito_id = Carrito_Detalle.objects.filter(session_key=request.session.session_key, producto_id=producto_id).first()                    
                    carrito_id.unidades = int(unidades_intoducida)
                    carrito_id.save()
                    producto_id.unidades = producto_id.unidades - int(unidades_intoducida )
                    producto_id.save()
                    titulo='Editar'
                    tipo='Info'
                    mensaje='Los datos se han guardado correctamente'
                
                if comando == "eliminar":
                    if request.user.is_authenticated:
                        carrito_id = Carrito_Detalle.objects.filter(user_id=request.user, producto_id=producto_id).first()
                    else:
                        carrito_id = Carrito_Detalle.objects.filter(session_key=request.session.session_key, producto_id=producto_id).first()
                    if carrito_id is not None:
                        carrito_id.delete() 
                    titulo='Eliminar'
                    tipo='Info'
                    mensaje='Producto eliminado' 
                request.session["add_contexto"]=dict(
                    toast=dict(
                        titulo=titulo,
                        tipo=tipo,
                        mensaje=mensaje,
                    ) 
               )                                          
                return redirect('cliente:carrito_list')
        except Exception as err:
            mensaje = err.args[0]
            request.session["add_contexto"]=dict(
                toast=dict(
                    titulo='Error',
                    tipo='Error',
                    mensaje=mensaje
                    )         
                )
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
                    request.session["add_contexto"]=dict(
                        toast=dict(
                            titulo="Guardar",
                            tipo="success",
                            mensaje='Los datos se han guardado correctamente',
                        ) 
                    )    
                return redirect(reverse('cliente:producto_detalle', kwargs=dict(key=key)))
    except Exception as err:
        mensaje = err.args[0]
        request.session["add_contexto"]=dict(
            toast=dict(
                titulo='Error',
                tipo='Error',
                mensaje=mensaje
                )         
            )
        return redirect('cliente:producto_list')      
            
        



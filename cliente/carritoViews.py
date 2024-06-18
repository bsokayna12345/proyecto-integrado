from decimal import Decimal
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
from main.models import  Direccion, Producto, SubCategoria
from django.shortcuts import render
from django.conf import settings
import uuid
from django.contrib.auth.models import User
    

class addirAlcarrito(TemplateView):
    """ Añadir producto a la cesta """
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
            
            # Asegurarse de que el carrito es un diccionario
            if isinstance(carrito, str):
                try:
                    carrito = json.loads(carrito)
                except json.JSONDecodeError:
                    carrito = {}
            
            # Comprobación de unidades
            if unidades > producto.unidades:
                titulo = "Añadir producto a la cesta"
                tipo = "Info"
                mensaje = "¡No hay suficientes unidades!"
            else:
                # Calcular el precio con IVA
                precio = Decimal(str(producto.precio)) if producto.precio else Decimal('0.0')
                iva = Decimal(str(producto.iva)) if producto.iva else Decimal('0.0')
                precio_con_iva = precio * (Decimal('1') + iva)
                
                # Calcular el precio de oferta (si aplica)
                if producto.en_oferta:
                    porcentaje = Decimal(str(producto.porcentaje)) if producto.porcentaje else Decimal('0.0')
                    porcentaje_oferta = porcentaje / Decimal('100.0')
                    precio_oferta = precio_con_iva * (Decimal('1') - porcentaje_oferta)
                else:
                    precio_oferta = Decimal('0.0')
                
                # Verificar si el producto ya está en el carrito
                if str(key) in carrito:
                    carrito[str(key)]['unidades'] += unidades
                else:
                    carrito[str(key)] = {
                        'nombre': producto.nombre,
                        'precio': str(precio),
                        'precio_oferta': str(precio_oferta) if precio_oferta else "",
                        'precio_con_iva': str(precio_con_iva),
                        'unidades': unidades,
                        'imagen': producto.get_Producto_ImagenProducto.first().imagen.url if producto.get_Producto_ImagenProducto.first() else ""
                    }
                
                titulo = "Añadir producto a la cesta"
                tipo = "success"
                mensaje = "Se ha añadido correctamente"
              
            request.session["add_contexto"] = dict(
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
            mensaje = str(err)
            request.session["add_contexto"] = dict(
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
        try:
            carrito = request.session.get('carrito', {})
            
            # Si el carrito está guardado como una cadena JSON, lo deserializamos
            if isinstance(carrito, str):          
                carrito = json.loads(carrito)
            
            total_carrito_sin_iva = 0  # Inicializa el subtotal del carrito
            total_carrito_con_iva = 0
            items_a_remover = []  # Lista de items a remover si no existen

            # Calcular el precio total por producto y el subtotal del carrito
            for item_id, item in list(carrito.items()):  # Convertimos a lista para modificar el diccionario mientras iteramos
                try:
                    producto = Producto.objects.get(id=item_id)
                    precio = producto.precio  # Precio del producto
                    iva = producto.iva                       
                    precio_con_iva = Decimal(str(precio)) * (Decimal('1') + Decimal(str(iva)))                                                                                                           
                    # Comprobar si el producto es de oferta                 
                    if producto.en_oferta:
                        porcentaje = producto.porcentaje
                        if porcentaje is not None:
                            porcentaje_oferta = Decimal(str(porcentaje)) / Decimal('100')
                            precio_oferta = precio_con_iva  * (Decimal('1') - porcentaje_oferta) 
                            item['precio_total_producto_con_iva'] = float(precio_oferta) * item['unidades']
                        else:
                            item['precio_total_producto_con_iva'] = float(precio_con_iva) * item['unidades']
                    else:
                        item['precio_total_producto_sin_iva'] = float(precio) * item['unidades']
                        item['precio_total_producto_con_iva'] = float(precio_con_iva) * item['unidades']
                    
                    item['id'] = producto.id
                    total_carrito_sin_iva += item.get('precio_total_producto_sin_iva', 0)
                    total_carrito_con_iva += item.get('precio_total_producto_con_iva', 0)
                except Producto.DoesNotExist:                
                    items_a_remover.append(item_id)
            
            # Remover productos no existentes del carrito
            for item_id in items_a_remover:
                del carrito[item_id]
            
            # Actualizar la sesión si hubo cambios
            if items_a_remover:
                request.session['carrito'] = json.dumps(carrito)

            # Preparar los ítems del carrito para PayPal
            cart_items = []
            subtotal = 0
            contador_productos = 0
            for item_id, item in carrito.items():
                try:
                    producto = Producto.objects.get(id=item_id)
                    precio = producto.precio  # Precio del producto
                    iva = producto.iva                       
                    precio_con_iva = Decimal(str(precio)) * (Decimal('1') + Decimal(str(iva))) 
                    item['marca'] = producto.marca_id.nombre
                    item['categoria'] = producto.subcategoria_id.categoria_id.nombre  
                    contador_productos += 1
                    if producto.en_oferta:
                        porcentaje = producto.porcentaje
                        if porcentaje is not None:
                            porcentaje_oferta = Decimal(str(porcentaje)) / Decimal('100')
                            precio_oferta = precio_con_iva * (Decimal('1') - porcentaje_oferta)               
                            precio_total = float(precio_oferta) * item['unidades']
                        else:
                            precio_total = float(precio_con_iva) * item['unidades']
                    else:
                        precio_total = float(precio_con_iva) * item['unidades']
                    
                    subtotal += precio_total            
                    cart_items.append({
                        'id': producto.id,
                        'name': producto.nombre,
                        'quantity': item['unidades'],
                        'price': float(precio_con_iva),
                    })
                    cart_items.append(dict(subtotal=float(subtotal)))
                except Producto.DoesNotExist:
                    continue
            
            # Comprobar si el usuario tiene dirección
            direccion = None
            if request.user.is_authenticated:
                usuario_id = request.user
                direccion = Direccion.objects.filter(user_id=usuario_id).first()

            contexto = {
                'carrito': carrito,
                'total_carrito_con_iva': total_carrito_con_iva,
                'total_carrito': total_carrito_sin_iva,
                'total_carrito_sin_iva': total_carrito_sin_iva,
                'cart_items': json.dumps(cart_items),
                'subtotal': subtotal,
                'direccion': direccion,
                'contador_productos': contador_productos
            }
            
            if request.session.get("add_contexto", None) is not None:
                contexto.update(request.session["add_contexto"])
                del request.session["add_contexto"]

            return render(request, self.template_name, contexto)
        except Exception as e:
            mensaje = str(e)
            request.session["add_contexto"] = {
                'toast': {
                    'titulo': 'Error',
                    'tipo': 'Error',
                    'mensaje': mensaje
                }
            }
            return render(request, self.template_name, {'error': mensaje})

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

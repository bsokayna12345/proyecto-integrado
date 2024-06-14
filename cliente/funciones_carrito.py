# from django.core import serializers
# from django.core.serializers import serialize
# from django.shortcuts import redirect, render
# from django.template.context_processors import request

# # from main.forms import FormUnidades
# from main.models import ItemCompra, Producto
# from django.core.serializers.json import DjangoJSONEncoder
# class LazyEncoder(DjangoJSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, Producto):
#             return str(obj)
#         return super().default(obj)

# '''
# Introduce un Itemcompra en la sesion
# session es un objeto django Session
# item_nuevo es un objeto del modelo ItemCompra
# '''
# def session_push(request, item_nuevo):
#     # request.session.flush()
#     listado_carrito = session_get(request)
#     if listado_carrito:  # Si existe un carro, deserializamos
#         item_old = getItem(listado_carrito, item_nuevo)
#         if item_old:
#             listado_carrito.remove(item_old)
#             item_old.unidades += item_nuevo.unidades
#             listado_carrito.add(item_old)
#             print(item_old)
#             print(listado_carrito)
#         else:
#             print("No existe")
#             listado_carrito.add(item_nuevo)
#     else:
#         listado_carrito.add(item_nuevo)
#         # Serializamos el listado de productos para guardar en sesion
#     serialize_and_save(request, listado_carrito)

# def getItem(listado_carrito, item):
#     if item in listado_carrito:
#         print("Existe")
#         for item_old in listado_carrito:
#             if item_old == item:
#                 return item_old

#     return None

# '''
# Devuelve un set de ItemCompra almacenado en sesion
# '''
# def session_get(request):
#     # request.session.flush()
#     productos_en_sesion = request.session.get('carrito', None)
#     print("Deseralizando!!")
#     listado_productos = set()
#     if productos_en_sesion:
#         for item_deserializado in serializers.deserialize('json', productos_en_sesion):
#             item_compra = item_deserializado.object
#             print(item_compra)
#             listado_productos.add(item_compra)

#     return listado_productos
# def serialize_and_save(request, listado_carrito):
#     productos_serializados = serialize('json', listado_carrito, cls=LazyEncoder)
#     request.session['carrito'] = productos_serializados
# def session_delete(request, item):

#     print("Eliminando")
#     listado_carrito = session_get(request)
#     listado_carrito.remove(item)
#     serialize_and_save(request, listado_carrito)




# def get_unidades(request, producto):
#     if request.method == 'GET':
#         form = FormUnidades(request.GET)
#         if form.is_valid():
#             unidades = form.cleaned_data['unidades']
#     return unidades

# def set_unidades(request, item,producto):
#     # lista de objetos del carrito
#     listado_carrito=session_get(request)
#     # devolver item_old que es  igual a item para modificar
#     item_old = getItem(listado_carrito,item)
#     # borrar el item_old del lista del  carrito
#     if item_old:
#         listado_carrito.remove(item_old)
#         unidades=get_unidades(request, producto)
#         # modificar las unidades del item old
#         item_old.unidades = unidades
#         print('item oldllllllllllllllll')
#         print(item_old)
#         # añadir el item al carrito
#         listado_carrito.add(item_old)
#         print(type(item_old))
#         print('naaaaaaaaaaaaaaaaaadaaaaaaaaaaaaa')
#     serialize_and_save(request,listado_carrito)


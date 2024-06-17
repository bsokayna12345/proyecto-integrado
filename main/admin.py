from django.contrib import admin
from .models import Marca, Producto, Categoria, SubCategoria, ImagenProducto, Perfil, Comentario, Pedido_detalle, Pedido_cabecera, Direccion
# Register your models here.
admin.site.register(Marca)
admin.site.register(Producto)
admin.site.register(Categoria)
admin.site.register(SubCategoria)
admin.site.register(ImagenProducto)
admin.site.register(Perfil)
admin.site.register(Comentario)
admin.site.register(Pedido_detalle)
admin.site.register(Pedido_cabecera)
admin.site.register(Direccion)




from django.contrib import admin
from .models import Marca, Producto, Categoria, SubCategoria, ImagenProducto
# Register your models here.
admin.site.register(Marca)
admin.site.register(Producto)
admin.site.register(Categoria)
admin.site.register(SubCategoria)
admin.site.register(ImagenProducto)


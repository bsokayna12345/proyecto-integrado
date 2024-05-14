
from django.contrib import admin
from django.urls import path
from administracion.filtrosView import filtro_subcategoria_categoria
from administracion.productoViews import ProductoEditPageView, ProductoListFilterPageView

from administracion.views import index
app_name="administracion"
urlpatterns = [   
    # path('', index, name='index'),
    path('', ProductoListFilterPageView.as_view(), name='producto_list'),
    path('administracion/producto-edit/<int:key>', ProductoEditPageView.as_view(), name='producto_edit'),
    path('administracion/producto-new/', ProductoEditPageView.as_view(), name='producto_new'),
    path('administracion/filtro-subcategoria/',filtro_subcategoria_categoria ),
]

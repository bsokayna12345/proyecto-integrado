
from django.contrib import admin
from django.urls import include, path
from cliente.carritoViews import CarritoListPageView, anadirAlCarrito
from cliente.inicioViews import ProductoDetalle, ProductoListPageView

app_name="cliente"
urlpatterns = [        
    path('', ProductoListPageView.as_view(), name='producto_list'),              
    path('producto-detalle/<int:key>', ProductoDetalle.as_view(), name="producto_detalle"),      
    path('carrito-list', CarritoListPageView.as_view(), name='carrito_list'),   
    path('carrito-edit/<int:key>', CarritoListPageView.as_view(), name='carrito_edit'),   
    # path('carrito-add/<int:key>', anadirAlCarrito, name="carrito_add"),      
]

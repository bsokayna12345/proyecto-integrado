
from django.contrib import admin
from django.urls import include, path
from cliente.inicioViews import ProductoListPageView
from cliente.views import index
app_name="cliente"
urlpatterns = [        
    path('', ProductoListPageView.as_view(), name='producto_list'),
    
]

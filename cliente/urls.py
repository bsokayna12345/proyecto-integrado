
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from cliente import views
from cliente.carritoViews import CarritoListPageView, anadirAlCarrito
from cliente.inicioViews import ProductoDetalle, ProductoListPageView
from cliente.loginViews import LoginView, logout_view
from cliente.perfilUsuarioViews import PerfileUsuarioEditView, PerfileUsuarioView
from cliente.registroUsuarioViews import RegistroUsuarioView

app_name="cliente"
urlpatterns = [            
    path('', ProductoListPageView.as_view(), name='producto_list'),              
    path('producto-list/<int:key_categoria>', ProductoListPageView.as_view(), name="producto_filter_categoria"),  
    path('producto-detalle/<int:key>', ProductoDetalle.as_view(), name="producto_detalle"),              
    path('carrito-list', CarritoListPageView.as_view(), name='carrito_list'),   
    path('carrito-edit/<int:key>', CarritoListPageView.as_view(), name='carrito_edit'),   
    path('perfil-usuario',PerfileUsuarioView.as_view(), name='perfile_usuario'),
    path('perfil-usuario-edit',PerfileUsuarioEditView.as_view(), name='perfile_usuario_edit'),
    path('registro-usuario',RegistroUsuarioView.as_view(), name='registro_usuario'),    
    path('login',LoginView.as_view(), name='login'),    
    path('logout',logout_view, name='logout'),
    # path('carrito-add/<int:key>', anadirAlCarrito, name="carrito_add"),      
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

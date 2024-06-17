
from django.contrib import admin
from django.urls import  path
from django.conf import settings
from django.conf.urls.static import static
from cliente import views
from cliente.carritoViews import  ModificarCarrito, MostrarCarrito, addirAlcarrito
from cliente.checkoutViews import CapturarOdernPaypal, CrearOrden, DetallesCompra
from cliente.inicioViews import ProductoBuscarListPageView, ProductoDetalle, ProductoListPageView
from cliente.loginViews import LoginView, logout_view
from cliente.ofertasViews import ProductoOfertaBuscarListPageView, ProductoOfertaListPageView
from cliente.perfilUsuarioViews import  PerfileUsuarioView
from cliente.registroUsuarioViews import RegistroUsuarioView


app_name="cliente"
urlpatterns = [            
    path('', ProductoListPageView.as_view(), name='producto_list'),              
    path('producto-list/<int:key_subcategoria>', ProductoListPageView.as_view(), name="producto_filter_subcategoria"),      
    path('producto-detalle/<int:key>', ProductoDetalle.as_view(), name="producto_detalle"),                  
    path('perfil-usuario',PerfileUsuarioView.as_view(), name='perfil_usuario'),
    path('perfil-usuario',PerfileUsuarioView.as_view(), name='perfil_usuario_edit'),
    path('registro-usuario',RegistroUsuarioView.as_view(), name='registro_usuario'),    
    path('login',LoginView.as_view(), name='login'),    
    path('logout',logout_view, name='logout'),   
    path('api/orders/', CrearOrden.as_view(),),
    path('api/orders/<order_id>/capture', CapturarOdernPaypal.as_view(),),
    path('carrito/<int:key_producto>', addirAlcarrito.as_view(), name="add_carrito"),
    path('mostrar-carrito', MostrarCarrito.as_view(), name="mostrar_carrito"),
    path('detalles-carrito/<int:order_id>/', DetallesCompra.as_view(), name="detalles_carrito"),
    path('modificar-carrito/<int:key_producto>', ModificarCarrito.as_view(), name="modificar_carrito"),
    path('producto-ofertas-list', ProductoOfertaListPageView.as_view(), name="oferta_list"),
    path('producto-oferta-list/<int:key_subcategoria>', ProductoOfertaListPageView.as_view(), name="producto_oferta_filter_categoria"),    
    path('producto-buscado-list', ProductoBuscarListPageView.as_view(), name="buscar"),    
    path('producto_oferta-buscado-list', ProductoOfertaBuscarListPageView.as_view(), name="buscar_oferta"), 
  

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

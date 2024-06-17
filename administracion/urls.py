
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from administracion.filtrosView import filtro_subcategoria_categoria
from administracion.loginViews import LoginView, logout_view
from administracion.pedidoViews import PedidoListFilterPageView
from administracion.usuariosView import UsuariosListFilterPageView
from cliente.perfilUsuarioViews import PerfileUsuarioView
from administracion.productoViews import EliminarImagen, ProductoAddPageView, ProductoEditPageView, ProductoListFilterPageView, SubirImagen
from django.contrib.auth import views as auth_views
from administracion.registroUsuarioViews import RegistroUsuarioView
from administracion.views import Index
app_name="administracion"
urlpatterns = [   
    path('', Index.as_view(), name='index'),
    path('producto-list', ProductoListFilterPageView.as_view(), name='producto_list'),
    path('producto-edit/<int:key>', ProductoEditPageView.as_view(), name='producto_edit'),
    path('producto-new/', ProductoAddPageView.as_view(), name='producto_new'),
    path('subir-imagen/<int:key_producto>/', SubirImagen.as_view(), name='subir_imagen'),
    path('eliminar-imagen/<int:key_imagen>/<int:key_producto>/', EliminarImagen.as_view(), name='eliminar_imagen'),
    path('filtro-subcategoria/',filtro_subcategoria_categoria ),    
    path('registro-usuario',RegistroUsuarioView.as_view(), name='registro_usuario'),
    path('perfil_usuario',PerfileUsuarioView.as_view(), name='perfil_usuario'),
    path('usuarios-list',UsuariosListFilterPageView.as_view(), name='usuarios_list' ),
    path('login',LoginView.as_view(), name='login'),    
    path('logout',logout_view, name='logout'),
    path('pedido-list', PedidoListFilterPageView.as_view(), name='pedido_list'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


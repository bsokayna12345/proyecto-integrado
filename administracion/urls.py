
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from administracion.filtrosView import filtro_subcategoria_categoria
from administracion.loginViews import LoginView, logout_view
from cliente.perfilUsuarioViews import PerfileUsuarioView
from administracion.productoViews import ProductoEditPageView, ProductoListFilterPageView, SubirImagen
from django.contrib.auth import views as auth_views
from administracion.registroUsuarioViews import RegistroUsuarioView
from administracion.views import index
app_name="administracion"
urlpatterns = [   
    path('', index, name='index'),
    path('producto-list', ProductoListFilterPageView.as_view(), name='producto_list'),
    path('producto-edit/<int:key>', ProductoEditPageView.as_view(), name='producto_edit'),
    path('producto-new/', ProductoEditPageView.as_view(), name='producto_new'),
    path('subir-imagen/<int:key_producto>/', SubirImagen.as_view(), name='subir_imagen'),
    path('filtro-subcategoria/',filtro_subcategoria_categoria ),    
    path('registro-usuario',RegistroUsuarioView.as_view(), name='registro_usuario'),
    path('perfil_usuario',PerfileUsuarioView.as_view(), name='perfil_usuario'),
    path('login',LoginView.as_view(), name='login'),    
    path('logout',logout_view, name='logout'),
  
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# path(
#         "change-password/",
#         auth_views.PasswordChangeView.as_view(template_name="change-password.html"),
#     ),
# accounts/login/ [name='login']
# accounts/logout/ [name='logout']
# accounts/password_change/ [name='password_change']
# accounts/password_change/done/ [name='password_change_done']
# accounts/password_reset/ [name='password_reset']
# accounts/password_reset/done/ [name='password_reset_done']
# accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']
# accounts/reset/done/ [name='password_reset_complete']

from django.contrib import admin
from django.urls import path
from administracion.filtrosView import filtro_subcategoria_categoria
from administracion.loginViews import LoginView, logout_view
from administracion.perfilUsuarioViews import PerfileUsuarioView
from administracion.productoViews import ProductoEditPageView, ProductoListFilterPageView
from django.contrib.auth import views as auth_views
from administracion.registroUsuarioViews import RegistroUsuarioView
from administracion.views import index
app_name="administracion"
urlpatterns = [   
    path('', index, name='index'),
    path('administracion/producto-list', ProductoListFilterPageView.as_view(), name='producto_list'),
    path('administracion/producto-edit/<int:key>', ProductoEditPageView.as_view(), name='producto_edit'),
    path('administracion/producto-new/', ProductoEditPageView.as_view(), name='producto_new'),
    path('administracion/filtro-subcategoria/',filtro_subcategoria_categoria ),
    path('administracion/registro-usuario',RegistroUsuarioView.as_view(), name='registro_usuario'),
    path('administracion/perfil_usuario/<int:key>',PerfileUsuarioView.as_view(), name='perfile_usuario'),
    path('administracion/login',LoginView.as_view(), name='login'),    
    path('administracion/logout',logout_view, name='logout'),
]
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
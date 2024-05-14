
from django.contrib import admin
from django.urls import include, path
from cliente.views import index
app_name="cliente"
urlpatterns = [   
    path('', index, name='index'),
]

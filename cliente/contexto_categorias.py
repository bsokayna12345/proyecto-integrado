from django.shortcuts import render
from main.models import Categoria


def categorias_disponibles(request):
    categorias = Categoria.objects.all()
    return {'categorias': categorias}
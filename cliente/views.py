from django.http import HttpResponse
from django.shortcuts import render

from main.models import Categoria

# Create your views here.
def index(request):
    return render(request=request, template_name='cliente/inicio.html')


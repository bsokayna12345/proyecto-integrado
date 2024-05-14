from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    try:
        return HttpResponse("desde cliente")
    except Exception as err:
        return err
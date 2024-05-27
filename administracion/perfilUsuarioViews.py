from django.shortcuts import render , redirect
from django.urls import reverse
from django.views.generic import TemplateView
from django.contrib.auth import get_user_model

from administracion.perfileUsuarioForms import PerfileUsuarioForm
from administracion.registroUsuarioForms import RegistroForm
from main.models import Perfil


class PerfileUsuarioView(TemplateView):
    template_name = "administracion/perfil-usuario.html"
    
    def contexto(self, request, perfel_id:Perfil): 
        try:
            contexto = dict(
                perfel_id=perfel_id,
                
            )
            return contexto
        except Exception as Err:
            return Err
     
    def get(self, request, *args, **kwargs):
        try:                
            # form = PerfileUsuarioForm()
            key = kwargs.get('key', None)
            if key is not None:                
                perfel_id = Perfil.objects.filter(id=key).first()
            else:
                perfel_id = None
            contexto = self.contexto(request, perfel_id=perfel_id)
            return render(request, self.template_name, contexto)
        
        except Exception as Err:            
            return Err
        
    
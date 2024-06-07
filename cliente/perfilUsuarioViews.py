from django.shortcuts import render , redirect
from django.urls import reverse
from django.views.generic import TemplateView
from django.contrib.auth import get_user_model

from cliente.perfileUsuarioForms import PerfileUsuarioForm
from administracion.registroUsuarioForms import RegistroForm
from main.models import Perfil


class PerfileUsuarioView(TemplateView):
    template_name = "cliente/perfil-usuario.html"
    
    def contexto(self, request, perfil_id:Perfil): 
        try:
            contexto = dict(
                perfil_id=perfil_id,
                
            )
            return contexto
        except Exception as Err:
            print(Err)
            return {}
     
    def get(self, request, *args, **kwargs):
        try:                                                                  
            perfil_id = Perfil.objects.filter(user_id = get_user_model().objects.get(id=request.user.id)).first()
            if perfil_id is None:
                perfil_id = None
            contexto = self.contexto(request, perfil_id=perfil_id)
            return render(request, self.template_name, contexto)
        
        except Exception as Err:            
            return Err
        
class PerfileUsuarioEditView(TemplateView):
    template_name = "cliente/perfil-usuario.html"
    
    def contexto(self, request, perfil_id:Perfil): 
        try:
            contexto = dict(
                perfil_id=perfil_id,
                
            )
            return contexto
        except Exception as Err:
            print(Err)
            return {}
     
    def get(self, request, *args, **kwargs):
        try:                                                                  
            perfil_id = Perfil.objects.filter(user_id = get_user_model().objects.get(id=request.user.id)).first()
            if perfil_id is None:
                perfil_id = None
            contexto = self.contexto(request, perfil_id=perfil_id)
            return render(request, self.template_name, contexto)
        
        except Exception as Err:            
            return Err
        
    
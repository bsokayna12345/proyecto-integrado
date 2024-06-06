from django import db
from django.shortcuts import render , redirect
from django.urls import reverse
from django.views.generic import TemplateView
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

from administracion.registroUsuarioForms import RegistroForm
from main.models import Perfil


class RegistroUsuarioView(TemplateView):
    template_name = "administracion/registro-usuario.html"
    
    def contexto(self, request, form:RegistroForm): 
        try:
            contexto = dict(
                form=form,
            )
            return contexto
        except Exception as Err:
            return Err
     
    def get(self, request, *args, **kwargs):
        try:                
            form = RegistroForm()
            contexto = self.contexto(request, form=form)
            return render(request, self.template_name, contexto)
        
        except Exception as Err:            
            return Err
        
    def post(self, request, *args, **kwargs):
        try:                        
            form = RegistroForm(request.POST)          
            with db.transaction.atomic():
                if form.is_valid(): 
                    usuario_id = get_user_model()(
                        first_name=form.cleaned_data["username"],
                        username=form.cleaned_data["email"],                        
                        last_name=form.cleaned_data["last_name"],                        
                        email= form.cleaned_data["email"],
                        password = make_password(form.cleaned_data["password1"]),
                    ) 
                    usuario_id.save()                              
                    perfil_id = Perfil(
                            user_id = usuario_id                   
                        )                    
                    perfil_id.save()       
                    return redirect(reverse('administracion:perfile_usuario'))
                else:
                    contexto = self.contexto(request, form=form)
            return render(request, self.template_name, contexto)                          
        except Exception as Err:
            print(Err)
            return redirect('administracion:registro_usuario')
                
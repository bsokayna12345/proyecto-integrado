from django import db
from django.shortcuts import render , redirect
from django.urls import reverse
from django.views.generic import TemplateView
from django.contrib.auth import get_user_model

from cliente.perfileUsuarioForms import PerfilEditForm, PerfileUsuarioForm
from administracion.registroUsuarioForms import RegistroForm
from main.models import Perfil

class PerfileUsuarioView(TemplateView):
    template_name = "cliente/perfil-usuario.html"
    
    def contexto(self, perfil_id, form): 
        try:
            contexto = {
                'perfil_id': perfil_id,
                'form': form,
            }
            return contexto
        except Exception as Err:
            print(Err)
            return {}
     
    def get(self, request, *args, **kwargs):
        try:
            perfil_id = Perfil.objects.filter(user_id=get_user_model().objects.get(id=request.user.id)).first()
            initial_data = {
                'nombre': perfil_id.user_id.first_name,
                'apellido': perfil_id.user_id.last_name,
                'movil': perfil_id.tel,
                'email': perfil_id.user_id.email,
            }
            form = PerfilEditForm(initial=initial_data)
            contexto = self.contexto(perfil_id, form)
            if request.session.get("add_contexto") is not None:
                contexto.update(request.session["add_contexto"])
                del request.session["add_contexto"]
            return render(request, self.template_name, contexto)
        
        except Exception as Err:            
            return render(request, 'error_template.html', {'mensaje': Err})
    
    def post(self, request, *args, **kwargs):
        try:
            perfil_id = Perfil.objects.filter(user_id=get_user_model().objects.get(id=request.user.id)).first()
            form = PerfilEditForm(request.POST, user=request.user)
            if form.is_valid():
                with db.transaction.atomic():
                    usuario_id = perfil_id.user_id
                    usuario_id.first_name = form.cleaned_data['nombre']
                    usuario_id.last_name = form.cleaned_data['apellido']
                    usuario_id.email = form.cleaned_data['email']
                    usuario_id.save()
                    
                    request.session["add_contexto"] = {
                        'toast': {
                            'titulo': "Editar perfil",
                            'tipo': "Info",
                            'mensaje': "Los datos se han guardado correctamente",
                        }
                    }
                    return redirect('cliente:perfil_usuario')
            else:
                contexto = self.contexto(perfil_id, form)
                return render(request, self.template_name, contexto)
        
        except Exception as Err:
            request.session["add_contexto"] = {
                'toast': {
                    'titulo': 'Error',
                    'tipo': 'Error',
                    'mensaje': str(Err),
                }
            }
            return redirect(reverse('cliente:perfil_usuario'))
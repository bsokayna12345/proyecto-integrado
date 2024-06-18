from django import db
from django.shortcuts import render , redirect
from django.urls import reverse
from django.views.generic import TemplateView
from django.contrib.auth import get_user_model

from cliente.perfileUsuarioForms import PerfilEditForm, PerfileUsuarioForm
from administracion.registroUsuarioForms import RegistroForm
from main.models import Direccion, Pedido_cabecera, Perfil

class PerfileUsuarioView(TemplateView):
    template_name = "cliente/perfil-usuario.html"
    
    def contexto(self,request, perfil_id, form): 
        try:
            qsProducto = Pedido_cabecera.objects.filter(usuario_id=request.user)            
            contexto = {
                'perfil_id': perfil_id,
                'form': form,
                'qsProducto':qsProducto,                
            }
            return contexto
        
        except Exception as Err:
            print(Err)
            return {}
     
    def get(self, request, *args, **kwargs):
        try:
            #TODO hay que controlar si el usuario es no o el usuario no tiene perfil por ejemplo en el caso de que sea sea el usuario admin            
            perfil_id = Perfil.objects.filter(user_id=request.user).first()
            direccion = None
            direccion_id = Direccion.objects.filter(user_id=request.user).first()
            if direccion_id is not None:
                direccion = direccion_id.direccion            
                initial_data = {
                    'nombre': perfil_id.user_id.first_name,
                    'apellido': perfil_id.user_id.last_name,
                    'movil': perfil_id.tel,
                    'email': perfil_id.user_id.email,
                    'direccion': direccion_id.direccion,
                    'codigo_postal':direccion_id.codigo_postal,
                    'pais':direccion_id.pais,
                    'provincia':direccion_id.provincia,             
                }
            else:
                initial_data = {
                    'nombre': perfil_id.user_id.first_name,
                    'apellido': perfil_id.user_id.last_name,
                    'movil': perfil_id.tel,
                    'email': perfil_id.user_id.email,                                                  
                }
            form = PerfilEditForm(initial=initial_data)
            contexto = self.contexto(request, perfil_id=perfil_id, form=form) 
            if request.session.get("add_contexto") is not None:
                contexto.update(request.session["add_contexto"])
                del request.session["add_contexto"]
            return render(request, self.template_name, contexto)
        
        except Exception as Err:  
            mensaje = Err.args[0]
            request.session["add_contexto"]=dict(
                toast=dict(
                    titulo='Error',
                    tipo='Error',
                    mensaje=mensaje                    
                    )         
                )
            return redirect(reverse('cliente:producto_list'))          
            
    
    def post(self, request, *args, **kwargs):
        try:
            perfil_id = Perfil.objects.filter(user_id=request.user).first()
            form = PerfilEditForm(request.POST, user=request.user)
            if form.is_valid():
                with db.transaction.atomic():
                    movil = request.POST.get('movil', None)
                    usuario_id = perfil_id.user_id
                    usuario_id.first_name = form.cleaned_data['nombre']
                    usuario_id.last_name = form.cleaned_data['apellido']
                    usuario_id.email = form.cleaned_data['email']
                    perfil_id.tel=movil                    
                    usuario_id.save()
                    perfil_id.save()
                    direccion = request.POST.get('direccion', None)                    
                    pais = request.POST.get('pais', None)
                    provincia = request.POST.get('provincia', None)
                    codigo_postal = request.POST.get('codigo_postal', None)
                    direccion_id = Direccion.objects.filter(user_id=usuario_id).first()
                    #modificar direccion
                    if direccion is not None and direccion_id is not None:
                        direccion_id.user_id = usuario_id
                        direccion_id.direccion = direccion   
                        direccion_id.codigo_postal = codigo_postal
                        direccion_id.pais= pais
                        direccion_id.provincia = provincia  
                        direccion_id.save()                  
                    else:
                        Direccion(
                            user_id=usuario_id,
                            direccion=direccion,
                            pais=pais,
                            provincia=provincia,
                            codigo_postal=codigo_postal,
                        ).save()               
                         
                    request.session["add_contexto"]=dict(
                        toast=dict(
                            titulo='Editar perfil',
                            tipo='Info',
                            mensaje="Los datos se han guardado correctamente"                    
                            )         
                        )               
                    return redirect('cliente:perfil_usuario')
            else:
                request.session["add_contexto"]=dict(
                    toast=dict(
                        titulo='Editar perfil',
                        tipo='Error',
                        mensaje="Por favor, revisa los errores del formulario y vuelve a intentarlo. "                    
                        )         
                    )
                contexto = self.contexto(request, perfil_id, form)
                return render(request, self.template_name, contexto)
        
        except Exception as Err:
            mensaje = Err.args[0]
            request.session["add_contexto"]=dict(
                toast=dict(
                    titulo='Error',
                    tipo='Error',
                    mensaje=mensaje                    
                    )         
                )
            return redirect(reverse('cliente:perfil_usuario'))


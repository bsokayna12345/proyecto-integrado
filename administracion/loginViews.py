import datetime
from django import db
from django.shortcuts import render , redirect
from django.urls import reverse
from django.contrib.auth import logout, get_user_model
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login


from administracion.loginForms import LoginForm
from main.models import Perfil


class LoginView(TemplateView):
    template_name = "administracion/login.html"
    
    def contexto(self, request,form:LoginForm): 
        try:
            contexto = dict(
                form=form,                
            )
            return contexto
        except Exception as Err:
            return Err
     
    def get(self, request, *args, **kwargs):
        try:                
            form = LoginForm()             
            contexto = self.contexto(request, form=form)
            return render(request, self.template_name, contexto)
        
        except Exception as Err:            
            return Err
    def post(self, request, *args, **kwargs):
        try:                        
            form = LoginForm(request.POST)  
            if form.is_valid():                               
                usuario_id = authenticate(username=form.cleaned_data["email"], password=form.cleaned_data["password"])       
                if usuario_id is not None:
                    # comprobar si el usuario esta bloqueado
                    perfil_id = Perfil.objects.filter(user_id=usuario_id).first()   
                    if perfil_id.bloqueado:
                        fecha = str(perfil_id.fecha_bloqueo)   
                        new_dt = fecha[:19]
                        fecha = datetime.strptime(new_dt, "%Y-%m-%d %H:%M:%S")
                        if fecha + datetime.timedelta(minutes=1) < datetime.now():
                            perfil_id.bloqueado = False                                
                            perfil_id.count = 0
                            perfil_id.fecha_bloqueo = None
                            perfil_id.save() 
                            return redirect(('administracion:login'))    
                        #TODO mensaje de que el usuario es blequeado                       
                    login(request, usuario_id)
                    return redirect('administracion:producto_list')                    
                else:
                    # usuario None
                    usuario_id = get_user_model().objects.filter(email=form.cleaned_data['email']).first()
                    if usuario_id:
                        perfil_id = Perfil.objects.filter(user_id=usuario_id)   
                        contador_intentos = perfil_id.count
                        if contador_intentos > 3:
                            perfil_id.bloqueado = True
                            perfil_id.fecha_bloqueo = datetime.now()
                            perfil_id.save()
                        else:
                            contador_intentos += 1
                            perfil_id.count = contador_intentos
                            perfil_id.save()
                    else:
                        # no existe el usuarrio 
                        #TODO mensaje de error en el coreo o la contraseña
                        return redirect(('administracion:login'))                                                                                                                                        
            return redirect(('administracion:login'))
        except Exception as Err:
            return Err
        
@login_required          
def logout_view(request):
    try:
        logout(request)    
        return redirect('administracion:index') 
    except Exception as Err:
            return Err
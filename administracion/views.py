# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView

# Create your views here.
def index(request):

    return render(request=request, template_name='administracion/index.html')


@method_decorator(login_required(login_url='administracion:login'), name='dispatch')  
class Index(TemplateView):
    """ Index  """
    template_name='administracion/index.html'  
     
    def get(self, request, *args, **kwargs):
        contexto = dict()     
        if request.user.is_superuser:
            return redirect('administracion:producto_list')
        request.session["add_contexto"]=dict(
                toast=dict(
                    titulo='Error',
                    tipo='Error',
                    mensaje='🚫 ¡Acceso denegado! Parece que no tienes poderes de superusuario. 🦸‍♂️ Solo los administradores pueden entrar aquí. 😅'
                    )         
                )    
        return redirect("administracion:login")
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
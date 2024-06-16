from django import db
from django.shortcuts import render , redirect
from django.urls import reverse
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


class UsuariosListFilterPageView(TemplateView):
    """ lista de Usuarios  """
    template_name='administracion/usuarios-list.html'
    def contexto(self, request, qsUsuarios:User): 
        try:
            contexto = dict(
                qsUsuarios=qsUsuarios,
            )
            return contexto
        except Exception as Err:
            return Err
     
    def get(self, request, *args, **kwargs):
        qsUsuarios = User.objects.all()
        contexto = self.contexto(request, qsUsuarios)
        if request.session.get("add_contexto", None) is not None:
            contexto.update(request.session["add_contexto"])
            del request.session["add_contexto"]
        return render(request, self.template_name, contexto)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

# administracion/permisos.py
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator

def superuser_required(view_func):
    """
    Decorador para requerir que el usuario sea un superusuario.
    """
    return user_passes_test(lambda u: u.is_superuser, login_url='administracion:login')(view_func)

def class_view_decorator(decorator):
    """
    Decorador para aplicar un decorador de función a todas las vistas en una clase basada en vistas.
    """
    def inner(cls):
        cls.dispatch = method_decorator(decorator)(cls.dispatch)
        return cls
    return inner
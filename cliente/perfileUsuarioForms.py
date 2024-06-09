from django import  forms
from main.models import Perfil
from django.contrib.auth.forms import User
from django.forms import ValidationError
import re


class PerfilEditForm(forms.Form):
    
    nombre = forms.CharField(        
        label="Nombre",      
        widget=forms.TextInput(attrs={"class": "form-control","placeholder":"nombre",}),
    )
      
    apellido = forms.CharField(
        label="Apellido",        
        widget=forms.TextInput(attrs={"class": "form-control","placeholder":"apellido",}),
    )
    movil = forms.CharField(
        required=False,
        label="Móvil",    
        widget=forms.TextInput(attrs={"class": "form-control","placeholder":"Móvil",}),
    )
    email = forms.EmailField(
        label="Correo electtronico",        
        widget=forms.EmailInput(attrs={"class": "form-control","placeholder":"correo electronico",}),
    )
    direccion = forms.CharField(
        required=False,
        label="Dirección",        
        widget=forms.TextInput(attrs={"class": "form-control","placeholder":"dirección",}),
    )

    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={"class": "form-control","placeholder":"Contraseña","autocomplete": "new-password"}),
    )
    password2 = forms.CharField(
        label="Confirmar Contraseña",
        widget=forms.PasswordInput(attrs={"class": "form-control","placeholder":"Confirmar Contraseña","autocomplete": "new-password"}),
        strip=False,       
    )   
    
    def clean_email(self):
        email1 = self.cleaned_data.get("email")
        print(email1)
        if User.objects.filter(email=email1).exists():
            raise ValidationError("El email ya esta registrado, prueba con otro.")
        return email1
    
    def clean_password2(self):
        """"""
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("contraseña no coincide")
        return password2
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        # Verificar la longitud del nombre de usuario
        if len(nombre) < 5 or len(nombre) > 15:
            raise forms.ValidationError("El nombre de usuario debe tener entre 5 y 15 caracteres.")

        # Verificar que el nombre de usuario no comience con un carácter especial
        if re.match(r'^[^a-zA-Z]', nombre):
            raise forms.ValidationError("El nombre de usuario debe comenzar con una letra.")        
        return nombre
        
    def clean_apellido(self):
        apellido = self.cleaned_data.get('apellido')
        # Verificar la longitud del apellido de usuario
        if len(apellido) < 5 or len(apellido) > 15:
            raise forms.ValidationError("El apellido de usuario debe tener entre 5 y 15 caracteres.")
        
        # Verificar que el apellido de usuario no comience con un carácter especial
        if re.match(r'^[^a-zA-Z]', apellido):
            raise forms.ValidationError("El apellido de usuario debe comenzar con una letra.")        
        return apellido
        

class PerfileUsuarioForm(forms.ModelForm):
          
          
    class Meta:
        model = Perfil
        fields = [
           'user_id'
        ]
        widgets = {
            'user_id' : forms.Select(attrs={"class": "form-control","placeholder":"Usuario"}),
            
        }
           

    
       
import re
from django import  forms
from django.contrib.auth.forms import User
from django.forms import ValidationError



class RegistroForm(forms.ModelForm):
    
    password1 = forms.CharField(
        label="Contraseña",
        strip=False,
        widget=forms.PasswordInput(attrs={"class": "form-control","placeholder":"Contraseña","autocomplete": "new-password"}),
    )
    password2 = forms.CharField(
        label="Confirmar Contraseña",
        widget=forms.PasswordInput(attrs={"class": "form-control","placeholder":"Confirmar Contraseña","autocomplete": "new-password"}),
        strip=False,       
    )   
    
    class Meta:
        model = User
        fields = [
            'username',
            'last_name',
            'email',
            'password1',
            'password2',
        ]
        widgets = {
            'username' : forms.TextInput(attrs={"class": "form-control","placeholder":"Nombre"}),
            'last_name' : forms.TextInput(attrs={"class": "form-control","placeholder":"Apellido"}),
            'email' : forms.EmailInput(attrs={"class": "form-control","placeholder":"Email"}),
        }
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
    def clean_username(self):
        username = self.cleaned_data.get('username')
        # Verificar la longitud del nombre de usuario
        if len(username) < 5 or len(username) > 15:
            raise forms.ValidationError("El nombre de usuario debe tener entre 5 y 15 caracteres.")

        # Verificar que el nombre de usuario no comience con un carácter especial
        if re.match(r'^[^a-zA-Z]', username):
            raise forms.ValidationError("El nombre de usuario debe comenzar con una letra.")        
        return username
        
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        # Verificar la longitud del apellido de usuario
        if len(last_name) < 5 or len(last_name) > 15:
            raise forms.ValidationError("El apellido de usuario debe tener entre 5 y 15 caracteres.")
        
        # Verificar que el apellido de usuario no comience con un carácter especial
        if re.match(r'^[^a-zA-Z]', last_name):
            raise forms.ValidationError("El apellido de usuario debe comenzar con una letra.")        
        return last_name
        
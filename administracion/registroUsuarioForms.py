from django import  forms
from django.contrib.auth.forms import User



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
        
    
        
        
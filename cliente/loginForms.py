from django import forms
from django.contrib.auth.forms import User

class LoginForm(forms.Form):
    
    email = forms.EmailField(label="Correo Electronico",
                             widget=forms.EmailInput(attrs={
                            'class':'form-control', 
                            }))
    password = forms.CharField(label="Contraseña",
                             widget=forms.PasswordInput(attrs={
                            'class':'form-control', 
                            }))
    class Meta:
        model = User
        fields = [
            'email',
            'password',
        ]
    
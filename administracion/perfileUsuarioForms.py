from django import  forms
from main.models import Perfil



class PerfileUsuarioForm(forms.ModelForm):
          
    class Meta:
        model = Perfil
        fields = [
           'user_id'
        ]
        widgets = {
            'user_id' : forms.Select(attrs={"class": "form-control","placeholder":"Usuario"}),
            
        }
           
    
       
# forms.py

from django import forms
from main.models import Comentario
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['contenido']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.template = 'bootstrap5/uni_form.html'
        self.helper.add_input(Submit('submit', 'Enviar'))

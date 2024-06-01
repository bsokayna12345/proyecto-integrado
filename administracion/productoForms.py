

from django import forms

from main.models import Marca, Producto, Categoria, SubCategoria

class ProductoForm(forms.ModelForm):

    onchange_categoria = "cargar_select('/administracion/filtro-subcategoria/', 'id_categoria_id', 'id_subcategoria_id','{text1}','{text2}','{text3}')".format(
        text1 = 'Seleccione una Categoria',
        text2 = 'No hay sub categorias para este categoria ',
        text3 = 'Seleccine primero una categoria'
    )
    
    categoria_id = forms.ModelChoiceField(
        queryset=Categoria.objects.all(),
        empty_label='Categoria',
        widget=forms.Select(
            attrs={'class':'form-control',"onchange":onchange_categoria}
        )
    )
    subcategoria_id = forms.ModelChoiceField(
        queryset=SubCategoria.objects.none(),
        empty_label='Sub Categoria',
        widget=forms.Select(
            attrs={'class':'form-control'}
        )
    )
    

    """ Model form de Producto"""
    class Meta:
        model = Producto
        fields = [          
            'subcategoria_id',   
            'marca_id',         
            'nombre',
            'precio',
            'iva',          
            'desccripcion',
            'unidades',
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control', 'placeholder':'nombre'}),
            'marca_id': forms.Select(attrs={'class':'form-control', 'placeholder':'marca_id'}),
            'precio': forms.TextInput(attrs={'class':'form-control',}),        
            'unidades': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'unidades'}),                        
            'iva': forms.TextInput(attrs={'class':'form-control'}),            
            'desccripcion': forms.Textarea(attrs={'class':'form-control',"cols": "40", "rows": "140","style": "height:90px;"}),             
        }

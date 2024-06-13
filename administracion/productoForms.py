

from django import forms

from main.models import ImagenProducto, Marca, Producto, Categoria, SubCategoria

class ProductoForm(forms.ModelForm):

    onchange_categoria = "cargar_select('/administracion/filtro-subcategoria/', 'id_categoria_id', 'id_subcategoria_id','{text1}','{text2}','{text3}')".format(
        text1 = 'Seleccione una Categoria',
        text2 = 'No hay sub categorias para este categoria ',
        text3 = 'Seleccine primero una categoria'
    )
    
    categoria_id = forms.ModelChoiceField(
        queryset=Categoria.objects.all(),       
        widget=forms.Select(
            attrs={'class':'form-control',"onchange":onchange_categoria}
        )
    )
    subcategoria_id = forms.ModelChoiceField(
        queryset=SubCategoria.objects.none(),       
        widget=forms.Select(
            attrs={'class':'form-control'}
        )
    )
    porcentaje = forms.IntegerField(
        required =False,  
        min_value=0,  
        max_value=100, 
        widget=forms.NumberInput(attrs={'class': 'form-control', 'title':'Introduce porcentaje ejemplo : 5', "style":"display:none;" })
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
            'en_oferta',
            "porcentaje",
            
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control', 'placeholder':'nombre'}),
            'marca_id': forms.Select(attrs={'class':'form-control', 'placeholder':'marca_id'}),
            'precio': forms.TextInput(attrs={'class':'form-control',}),                   
            'unidades': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'unidades'}),                        
            'iva': forms.TextInput(attrs={'class':'form-control'}),       
            'en_oferta': forms.CheckboxInput(attrs={'class': 'form-check',"style": "margin: 10px;  transform: scale(1.5)", 
                                                     "data-toggle":"tooltip", "data-placement":"left",
                                                    'title': '¿Está este producto en oferta? Haz clic para marcar esta opción' ,"required":False}),  
            'desccripcion': forms.Textarea(attrs={'class':'form-control',"cols": "40", "rows": "140","style": "height:90px;"}),             
        }

class ImagenForm(forms.ModelForm):

    class Meta:
        model = ImagenProducto
        fields = [ 
            "imagen",
            "imagen_principal",
        ]
        widgets = {
             'imagen_principal': forms.CheckboxInput(attrs={'class': 'form-check',"style": "margin: 10px;  transform: scale(1.5)", 
                                                     "data-toggle":"tooltip", "data-placement":"left",
                                                    'title': '!Haz click si Quieres establecer la imagen como una imagen principal.' ,"required":False}),  
            'imagen': forms.ClearableFileInput(attrs={
                'class': 'form-control-file',
                'style': 'margin: 10px;',
                'data-toggle': 'tooltip',
                'data-placement': 'left',
                'title': 'Sube una imagen para el producto'
            }),
        }
       


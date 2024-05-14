from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import  MinValueValidator
# Create your models here.

class Marca(models.Model):
    id = models.AutoField(db_column="id", primary_key=True, verbose_name=_('ID'))
    nombre = models.CharField(max_length=20, unique=True)

    def __str__(self) -> str:
        return self.nombre
    class Meta:
        db_table = "t_marca"
        verbose_name = "Marca"
        verbose_name_plural ="Marcas"     
        constraints = [
            models.UniqueConstraint(name='marca_uk-c', fields=['nombre'])
        ]


class Categoria(models.Model):
    id = models.AutoField(db_column="id", primary_key=True, verbose_name=_('ID'))
    nombre = models.CharField(max_length=20, unique=True)
    
    def __str__(self) -> str:
        return self.nombre
    class Meta:
        db_table = "t_categoria"
        verbose_name = "Categoria"
        verbose_name_plural ="Categorias"
        

class SubCategoria(models.Model):
    id = models.AutoField(db_column="id", primary_key=True, verbose_name=_('ID'))
    nombre = models.CharField(max_length=20, unique=True)
    categoria_id = models.ForeignKey(db_column='categoria_id', to=Categoria, on_delete=models.CASCADE, related_name='get_Categoria_SubCategoria', verbose_name=_("Categoria"))
    
    def __str__(self) -> str:
        return self.nombre
    
    class Meta:
        db_table = "t_subcategoria"
        verbose_name = "Sub Categoria"
        verbose_name_plural ="Sub Categorias"


class Producto(models.Model):
    id = models.AutoField(db_column="id", primary_key=True, verbose_name=_('ID'))    
    nombre = models.CharField(max_length=200,  )
    precio = models.DecimalField(decimal_places=2, max_digits=8, validators=[MinValueValidator(0.00)])
    iva = models.DecimalField(default=0.21, decimal_places=2, max_digits=5, validators=[MinValueValidator(0.00)])
    desccripcion = models.TextField(null=True, blank=True)    
    subcategoria_id = models.ForeignKey(db_column='sucategoria_id', to=SubCategoria, on_delete=models.CASCADE, related_name='get_SubCategoria_Producto', verbose_name=_("SubCategoria"))    
    marca_id = models.ForeignKey(db_column='marca_id', to=Marca, on_delete=models.CASCADE, related_name='get_Marca_Producto', verbose_name=_("Marca"))
    def __str__(self) -> str:
        return self.nombre
    
    class Meta:
        db_table = "t_producto"
        verbose_name = "Producto"
        verbose_name_plural ="Productos"

class ImagenProducto(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    imagen = models.ImageField(upload_to='producto/imagenes', null=True, blank=True)
    producto_id = models.ForeignKey(db_column='producto_id', to=Producto, on_delete=models.CASCADE, related_name='get_Producto_ImagenProducto', verbose_name=_("Producto"))

    def __str__(self) -> str:
        return f"{self.imagen}-{self.producto_id}"
    
    class Meta:
        db_table = "t_imagen_producto"
        verbose_name = "Imagen Producto"
        verbose_name_plural ="Imagens Producto"

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import  MinValueValidator
from django.db.models import UniqueConstraint
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
        db_table = "categoria"
        verbose_name = "Categoria"
        verbose_name_plural ="Categorias"
        

class SubCategoria(models.Model):
    id = models.AutoField(db_column="id", primary_key=True, verbose_name=_('ID'))
    nombre = models.CharField(max_length=20, unique=True)
    categoria_id = models.ForeignKey(db_column='categoria_id', to=Categoria, on_delete=models.CASCADE, related_name='get_Categoria_SubCategoria', verbose_name=_("Categoria"))
    
    def __str__(self) -> str:
        return self.nombre
    
    class Meta:
        db_table = "subcategoria"
        verbose_name = "Sub Categoria"
        verbose_name_plural ="Sub Categorias"


class Producto(models.Model):
    id = models.AutoField(db_column="id", primary_key=True, verbose_name=_('ID'))    
    nombre = models.CharField(max_length=200,  )
    precio = models.DecimalField(decimal_places=2, max_digits=8, validators=[MinValueValidator(0.00)])
    unidades = models.PositiveIntegerField(default=0)
    iva = models.DecimalField(default=0.21, decimal_places=2, max_digits=5, validators=[MinValueValidator(0.00)])
    desccripcion = models.TextField(null=True, blank=True)    
    subcategoria_id = models.ForeignKey(db_column='sucategoria_id', to=SubCategoria, on_delete=models.CASCADE, related_name='get_SubCategoria_Producto', verbose_name=_("SubCategoria"))    
    marca_id = models.ForeignKey(db_column='marca_id', to=Marca, on_delete=models.CASCADE, related_name='get_Marca_Producto', verbose_name=_("Marca"))
    
    def __str__(self) -> str:
        return self.nombre
    
    class Meta:
        db_table = "producto"
        verbose_name = "Producto"
        verbose_name_plural ="Productos"

class ImagenProducto(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    imagen = models.ImageField(upload_to='producto/imagenes', null=True, blank=True)
    producto_id = models.ForeignKey(db_column='producto_id', to=Producto, on_delete=models.CASCADE, related_name='get_Producto_ImagenProducto', verbose_name=_("Producto"))

    def __str__(self) -> str:
        return f"{self.imagen}-{self.producto_id}"
    
    class Meta:
        db_table = "imagen_producto"
        verbose_name = "Imagen Producto"
        verbose_name_plural ="Imagens Producto"

class Perfil(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    user_id = models.OneToOneField(db_column='', to=settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, related_name="get_Profile_User")
    dni = models.CharField(max_length=9)
    tel = models.CharField(max_length=12, null=True, blank=True)
    imagen = models.ImageField(upload_to="imagen_profile/", null=True, blank=True)
    count = models.PositiveIntegerField(default=0)
    fecha_bloqueo = models.DateTimeField(null=True, blank=True)
    bloqueado = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return f"{self.user_id}-{self.user_id.username}"
    
    class Meta:
        db_table = "perfil"
        verbose_name = "perfil"
        verbose_name_plural ="Perfiles"
        
class Direccion(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    user_id = models.OneToOneField(db_column='', to=settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, related_name="get_Direccion_User")
    pais =  models.CharField(max_length=200, null=True) 
    direccion = models.CharField(max_length=200, null=True)
    provincia = models.CharField(max_length=200, null=True)
    codigo_postal = models.CharField(max_length=200, null=True)
    es_entrega = models.BooleanField(default=True)
    
    def __str__(self) -> str:
        return f"{self.user_id.username}-{self.direccion}"
    
    class Meta:
        db_table = "direccion"
        verbose_name = "Direccion"
        verbose_name_plural ="Direcciones"



class Carrito_Detalle(models.Model):
    user_id = models.ForeignKey(db_column='usuario_id', to=settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, related_name='get_user_carrito')
    producto_id = models.ForeignKey(to=Producto , on_delete=models.RESTRICT, related_name='get_producto_carrito')
    unidades = models.IntegerField()
    
    class Meta:
        db_table = 'carrito_Detalle'
        verbose_name = 'Carrito detalla'
        verbose_name_plural = 'Carritos Detalles'

        UniqueConstraint(fields=['user_id', 'producto_id'], name='unique_user_producto_id'),
        constraints = [
            models.UniqueConstraint(name='unique_user_producto_id', fields=['user_id', 'producto_id'])
        ]
    def __str__(self):
        return f"{self.user_id}-{self.producto_id}-{self.unidades}"
    

class Pedido_cabecera(models.Model):
    id = models.AutoField(primary_key=True)
    usuario_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT)    
    fecha=models.DateField(auto_now_add=True)
    direccion_entrega_id = models.ForeignKey(to=Direccion, null=True, on_delete=models.RESTRICT, related_name='get_direccion_e_pedidoCabecera')    

    class Meta:
        db_table = 'pedido_cabecera'
        verbose_name = "Pedido_cabecera"
        verbose_name_plural = "Pedidos_cebeceras"

    def __str__(self):
        return str(' usuario id : '+self.usuario_id + ', metodo de pago id : '+ self.metodo_pago_id + ', item: '+ self.item)


class Pedido_detalle(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200)
    producto_id =  models.ForeignKey(to=Producto, on_delete=models.RESTRICT, related_name='get_productos_pedidos')
    precio = models.DecimalField(max_digits= 8, decimal_places=2, validators=[MinValueValidator(0.00)])
    unidades = models.PositiveIntegerField()
    descripcion = models.TextField(null=True, blank=True)
    iva = models.DecimalField(max_digits= 8, decimal_places=2,validators=[MinValueValidator(0.00)])
    
    class Meta:
        db_table = 'pedido_detalle'
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ['-nombre']
    
    def __str__(self):        
        return f"{self.producto_id}-{self.nombre}"
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Producto

# @receiver(post_save, sender=Producto)
# def calcular_precio_con_iva(sender, instance, **kwargs):
#     precio_final = instance.precio_oferta if instance.en_oferta and instance.precio_oferta else instance.precio
#     instance.precio_con_iva = precio_final + (precio_final * instance.iva)
#     instance.save()
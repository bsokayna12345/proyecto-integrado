# Generated by Django 5.0.4 on 2024-05-31 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_carrito_detalle_unique_user_producto_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='unidades',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
# Generated by Django 5.0.4 on 2024-05-27 17:18

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_direccion_perfil'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='direccion',
            options={'verbose_name': 'Direccion', 'verbose_name_plural': 'Direcciones'},
        ),
        migrations.AlterModelTable(
            name='categoria',
            table='categoria',
        ),
        migrations.AlterModelTable(
            name='direccion',
            table='direccion',
        ),
        migrations.AlterModelTable(
            name='imagenproducto',
            table='imagen_producto',
        ),
        migrations.AlterModelTable(
            name='perfil',
            table='perfil',
        ),
        migrations.AlterModelTable(
            name='producto',
            table='producto',
        ),
        migrations.AlterModelTable(
            name='subcategoria',
            table='subcategoria',
        ),
        migrations.CreateModel(
            name='Carrito_Detalle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unidades', models.IntegerField()),
                ('producto_id', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='get_producto_carrito', to='main.producto')),
                ('user_id', models.ForeignKey(db_column='usuario_id', on_delete=django.db.models.deletion.RESTRICT, related_name='get_user_carrito', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Carrito detalla',
                'verbose_name_plural': 'Carritos Detalles',
                'db_table': 'carrito_Detalle',
            },
        ),
        migrations.CreateModel(
            name='Pedido_cabecera',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fecha', models.DateField(auto_now_add=True)),
                ('direccion_entrega_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='get_direccion_e_pedidoCabecera', to='main.direccion')),
                ('usuario_id', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Pedido_cabecera',
                'verbose_name_plural': 'Pedidos_cebeceras',
                'db_table': 'pedido_cabecera',
            },
        ),
        migrations.CreateModel(
            name='Pedido_detalle',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=200)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('unidades', models.PositiveIntegerField()),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('iva', models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('producto_id', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='get_productos_pedidos', to='main.producto')),
            ],
            options={
                'verbose_name': 'Pedido',
                'verbose_name_plural': 'Pedidos',
                'db_table': 'pedido_detalle',
                'ordering': ['-nombre'],
            },
        ),
    ]
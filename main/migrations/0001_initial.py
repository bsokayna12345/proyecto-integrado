# Generated by Django 5.0.4 on 2024-05-14 17:17

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.AutoField(db_column='id', primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=20, unique=True)),
            ],
            options={
                'verbose_name': 'Categoria',
                'verbose_name_plural': 'Categorias',
                'db_table': 't_categoria',
            },
        ),
        migrations.CreateModel(
            name='ImagenProducto',
            fields=[
                ('id', models.AutoField(db_column='id', primary_key=True, serialize=False)),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='producto/imagenes')),
            ],
            options={
                'verbose_name': 'Imagen Producto',
                'verbose_name_plural': 'Imagens Producto',
                'db_table': 't_imagen_producto',
            },
        ),
        migrations.CreateModel(
            name='Marca',
            fields=[
                ('id', models.AutoField(db_column='id', primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=20, unique=True)),
            ],
            options={
                'verbose_name': 'Marca',
                'verbose_name_plural': 'Marcas',
                'db_table': 't_marca',
            },
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.AutoField(db_column='id', primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('iva', models.DecimalField(decimal_places=2, default=0.21, max_digits=5, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('desccripcion', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Producto',
                'verbose_name_plural': 'Productos',
                'db_table': 't_producto',
            },
        ),
        migrations.CreateModel(
            name='SubCategoria',
            fields=[
                ('id', models.AutoField(db_column='id', primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=20, unique=True)),
            ],
            options={
                'verbose_name': 'Sub Categoria',
                'verbose_name_plural': 'Sub Categorias',
                'db_table': 't_subcategoria',
            },
        ),
        migrations.AddConstraint(
            model_name='marca',
            constraint=models.UniqueConstraint(fields=('nombre',), name='marca_uk-c'),
        ),
        migrations.AddField(
            model_name='producto',
            name='marca_id',
            field=models.ForeignKey(db_column='marca_id', on_delete=django.db.models.deletion.CASCADE, related_name='get_Marca_Producto', to='main.marca', verbose_name='Marca'),
        ),
        migrations.AddField(
            model_name='imagenproducto',
            name='producto_id',
            field=models.ForeignKey(db_column='producto_id', on_delete=django.db.models.deletion.CASCADE, related_name='get_Producto_ImagenProducto', to='main.producto', verbose_name='Producto'),
        ),
        migrations.AddField(
            model_name='subcategoria',
            name='categoria_id',
            field=models.ForeignKey(db_column='categoria_id', on_delete=django.db.models.deletion.CASCADE, related_name='get_Categoria_SubCategoria', to='main.categoria', verbose_name='Categoria'),
        ),
        migrations.AddField(
            model_name='producto',
            name='subcategoria_id',
            field=models.ForeignKey(db_column='sucategoria_id', on_delete=django.db.models.deletion.CASCADE, related_name='get_SubCategoria_Producto', to='main.subcategoria', verbose_name='SubCategoria'),
        ),
    ]

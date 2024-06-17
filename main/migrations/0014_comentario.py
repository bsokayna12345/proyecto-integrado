# Generated by Django 5.0.4 on 2024-06-16 21:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_remove_producto_precio_con_iva_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.AutoField(db_column='id', primary_key=True, serialize=False)),
                ('contenido', models.TextField(verbose_name='Contenido')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('producto_id', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='get_Comentario_Producto', to='main.producto')),
                ('usuario_id', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='get_Comentario_User', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Comentario',
                'verbose_name_plural': 'Comentarios',
                'db_table': 'comentario',
            },
        ),
    ]
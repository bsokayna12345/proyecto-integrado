# Generated by Django 5.0.4 on 2024-06-08 10:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_perfil_unique_user_id'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='carrito_detalle',
            name='session_key',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='carrito_detalle',
            name='user_id',
            field=models.ForeignKey(blank=True, db_column='usuario_id', null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='get_user_carrito', to=settings.AUTH_USER_MODEL),
        ),
    ]

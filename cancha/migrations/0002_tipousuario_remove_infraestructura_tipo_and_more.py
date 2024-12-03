# Generated by Django 5.1 on 2024-11-05 13:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cancha', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TipoUsuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('descripcion', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'tipo_usuario',
            },
        ),
        migrations.RemoveField(
            model_name='infraestructura',
            name='tipo',
        ),
        migrations.AlterField(
            model_name='reserva',
            name='deporte',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cancha.deporte'),
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('clave', models.CharField(max_length=45)),
                ('tipo_usuario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='usuarios', to='cancha.tipousuario')),
            ],
            options={
                'db_table': 'usuario',
            },
        ),
        migrations.AlterField(
            model_name='reserva',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cancha.usuario'),
        ),
    ]
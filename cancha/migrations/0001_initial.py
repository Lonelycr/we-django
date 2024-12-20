# Generated by Django 5.1.1 on 2024-10-24 21:45

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Deporte',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique=True)),
                ('logo', models.ImageField(upload_to='logos/')),
            ],
            options={
                'db_table': 'deporte',
            },
        ),
        migrations.CreateModel(
            name='Infraestructura',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('tipo', models.CharField(max_length=50)),
                ('capacidad', models.IntegerField()),
                ('descripcion', models.TextField()),
                ('horarios', models.CharField(max_length=50)),
                ('precio', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('foto', models.ImageField(blank=True, null=True, upload_to='infraestructuras/')),
                ('deporte', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='infraestructuras', to='cancha.deporte')),
            ],
            options={
                'db_table': 'infraestructura',
            },
        ),
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deporte', models.CharField(choices=[('futbol', 'Fútbol'), ('tenis', 'Tenis'), ('padel', 'Pádel'), ('basketball', 'Baloncesto'), ('golf', 'Golf'), ('volleyball', 'Voleibol')], max_length=20)),
                ('fecha', models.DateField()),
                ('horario', models.TimeField()),
                ('infraestructura', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cancha.infraestructura')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'reserva',
            },
        ),
    ]

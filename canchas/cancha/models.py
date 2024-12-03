from django.db import models
from django.contrib.auth.models import User

class Deporte(models.Model):
    nombre = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    logo = models.ImageField(upload_to='logos/')

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'deporte'


class Infraestructura(models.Model):
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50)
    capacidad = models.IntegerField()
    descripcion = models.TextField()
    horarios = models.CharField(max_length=50)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    foto = models.ImageField(upload_to='infraestructuras/', blank=True, null=True)

    # Relación con Deporte
    deporte = models.ForeignKey(Deporte, on_delete=models.CASCADE, related_name='infraestructuras')

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'infraestructura'


class Reserva(models.Model):
    infraestructura = models.ForeignKey(Infraestructura, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateField()
    horario = models.TimeField()
    deporte = models.ForeignKey(Deporte, on_delete=models.CASCADE)
    precio_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # Nuevo campo

    class Meta:
        db_table = 'reserva'


class TipoUsuario(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'tipo_usuario'

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    clave = models.CharField(max_length=45)
    tipo_usuario = models.ForeignKey(
        'TipoUsuario', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='usuarios'
    )

    def __str__(self):
        return self.nombre
    
    class Meta:
        db_table = 'usuario'

class Descuento(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    porcentaje = models.DecimalField(max_digits=5, decimal_places=2)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.codigo} ({self.porcentaje}%)"
    
    class Meta:
        db_table = 'descuento'
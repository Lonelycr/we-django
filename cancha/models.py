from django.db import models
from django.utils import timezone 

class Deporte(models.Model):
    nombre = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    logo = models.ImageField(upload_to='logos/')

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'deporte'

class Infraestructura(models.Model):
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('mantenimiento', 'En Mantenimiento'),
        ('inactivo', 'Inactivo'),
        ('reparacion', 'En Reparación'),
    ]

    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50)
    capacidad = models.IntegerField()
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    foto = models.ImageField(upload_to='infraestructuras/', blank=True, null=True)
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='activo'
    )
    deporte = models.ForeignKey(Deporte, on_delete=models.CASCADE, related_name='infraestructuras')

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'infraestructura'

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
    codigo = models.CharField(max_length=50,unique=True)
    porcentaje = models.DecimalField(max_digits=5,decimal_places=2)
    activo = models.BooleanField(default=True)
    fecha_expiracion = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.codigo} ({self.porcentaje})"
    
    class Meta:
        db_table = 'descuento'

class Reserva(models.Model):
    infraestructura = models.ForeignKey(Infraestructura, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora_inicio = models.TimeField() 
    hora_fin = models.TimeField()     
    deporte = models.ForeignKey(Deporte, on_delete=models.CASCADE)
    horario = models.TimeField(null=True, blank=True)
    precio_total = models.DecimalField(max_digits=1000,decimal_places=2,default=0.0) 
    descuento = models.ForeignKey(Descuento, null=True, blank=True, on_delete=models.SET_NULL)

    def aplicar_descuento(self):
        if self.descuento and self.descuento.activo and (self.descuento.fecha_expiracion is None or self.descuento.fecha_expiracion > timezone.now()):
            descuento = self.descuento.porcentaje / 100
            self.precio_total -= self.precio_total * descuento
        else:
            self.precio_total = self.precio_total
    
    class Meta:
        db_table = 'reserva'


class Horario(models.Model):
    infraestructura = models.ForeignKey(Infraestructura, related_name='horarios', on_delete=models.CASCADE)
    dia_semana = models.CharField(
        max_length=9,
        choices=[('lunes', 'Lunes'), ('martes', 'Martes'), ('miércoles', 'Miércoles'),
                 ('jueves', 'Jueves'), ('viernes', 'Viernes'), ('sábado', 'Sábado'),
                 ('domingo', 'Domingo')],
    )
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    def __str__(self):
        return f"{self.dia_semana} {self.hora_inicio}-{self.hora_fin} - {self.infraestructura.nombre}"
    

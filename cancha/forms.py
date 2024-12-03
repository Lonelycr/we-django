from django import forms
from .models import Infraestructura, Reserva, Deporte, Horario
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth.models import User
from datetime import datetime,  timedelta 

class InfraestructuraForm(forms.ModelForm):
    class Meta:
        model = Infraestructura
        fields = ['nombre', 'tipo', 'capacidad', 'descripcion', 'precio', 'foto', 'estado', 'deporte']

class ReservaEditForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['infraestructura', 'usuario', 'fecha', 'hora_inicio', 'hora_fin', 'deporte']

    def clean(self):
        cleaned_data = super().clean()
        fecha = cleaned_data.get('fecha')
        hora_inicio = cleaned_data.get('hora_inicio')
        infraestructura = cleaned_data.get('infraestructura')

        # Validar que no haya reservas solapadas
        if fecha and hora_inicio and infraestructura:
            hora_fin = (datetime.combine(datetime.today(), hora_inicio) + timedelta(hours=1)).time()
            if Reserva.objects.filter(
                infraestructura=infraestructura,
                fecha=fecha,
                hora_inicio__lt=hora_fin,
                hora_fin__gt=hora_inicio
            ).exists():
                raise forms.ValidationError("Ya existe una reserva para esta infraestructura, fecha y hora.")

        return cleaned_data

class DeporteForm(forms.ModelForm):
    class Meta:
        model = Deporte
        fields = ['nombre', 'logo', 'slug']

class LoginForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=100)
    clave = forms.CharField(label='Clave', max_length=45, widget=forms.PasswordInput)

class HorarioForm(forms.ModelForm):
    class Meta:
        model = Horario
        fields = ['infraestructura', 'dia_semana', 'hora_inicio', 'hora_fin']
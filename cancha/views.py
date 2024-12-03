from django.shortcuts import render, redirect,get_object_or_404
from .models import Reserva, Infraestructura, Deporte, Usuario, Descuento
from .forms import Infraestructura, DeporteForm, LoginForm
from django.contrib import messages
from datetime import datetime,  timedelta, timezone, date
from django.db.models import Q
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.utils import timezone 

def inicio(request):
    deportes = Deporte.objects.all() # Obtiene todos los objetos de la clase 'deporte' de la base de datos y los almacena en 'deportes'.
    usuario_id = request.session.get('usuario_id') # Intenta recuperar el ID del usuario almacenado en la sesión.
    if usuario_id: # Si el usuario está en sesión:
        try:
            usuario = Usuario.objects.get(id=usuario_id) # Obtiene el objeto 'Usuario' correspondiente y , si el usuario tiene existe.
            tipo_usuario_id = usuario.tipo_usuario_id # Obtenemos el ID del tipo de usuario
        except Usuario.DoesNotExist:# Si no se encuentra al usuario, establece 'usuario' y 'tipo_usuario_id' en 'NONE'.
            usuario = None
            tipo_usuario_id = None
    else:
        usuario = None
        tipo_usuario_id = None #Si no hay un usuario en sesion, se asigna 'None'  tanto a 'usuario' como a 'tipo_usuario_id'.

    return render(request, 'cancha/inicio.html', { #Retorna el renderizao de la plantilla 'cancha/inicio.html', pasando al contexto:
        'deportes': deportes,
        'usuario': usuario,
        'tipo_usuario_id': tipo_usuario_id  # Pasamos tipo_usuario_id al contexto.
    })


def iniciar_sesion(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)  # Crea un formulario `LoginForm` con los datos enviados.
        if form.is_valid():  # Si el formulario es válido:
            email = form.cleaned_data['email']  # Extrae el email
            clave = form.cleaned_data['clave']  # Y la clave proporcionados.
            try:
                usuario = Usuario.objects.get(email=email, clave=clave)  # Intenta buscar un usuario en la base de datos con el email y la clave ingresados.
                request.session['usuario_id'] = usuario.id  # Si encuentra al usuario, guarda su ID en la sesión.
                
                # Manejo del parámetro next para redirigir a la URL deseada
                next_url = request.GET.get('next')  # Verifica si hay un parámetro `next` en la URL.
                if next_url:
                    return redirect(next_url)  # Si `next` está presente, redirige a esa URL.
                return redirect('inicio')  # Si no, redirige a la vista de `inicio`.
            
            except Usuario.DoesNotExist:  # Si no encuentra al usuario:
                messages.error(request, 'Credenciales incorrectas. Inténtalo de nuevo.')  # Muestra un mensaje de error.
    else:
        form = LoginForm()  # Si el método de la solicitud no es `POST`, crea un formulario vacío.

    return render(request, 'cancha/iniciar_sesion.html', {'form': form})  # Retorna a `iniciar_sesion.html`.

def cerrar_sesion(request):
    request.session.pop('usuario_id', None) # Eliminar el ID del usuario de la sesión
    return redirect('inicio')# Retorna al inicio.

def perfil(request):
    usuario_id = request.session.get('usuario_id')# Obtiene el 'usuario_id' en la sesión actual.
    if usuario_id:# Si 'usuario_id' esta presenta en la sesión, significa que el usuario esta autenticado.
        try:
            usuario = Usuario.objects.get(id=usuario_id)  # Intenta obtener el usuario desde la base de datos utilizando el 'usuario_id'.
            return render(request, 'cancha/perfil.html', {'usuario': usuario})# Si el usuario existe, se renderiza a la plantilla 'canchas/perfil.html'.
        except Usuario.DoesNotExist: # Si el 'usuario_id' no está en la sesión, significa que el usuario no ha iniciado sesión.
            return redirect('inicio')  # Y redirige a inicio.
    else:
        return redirect('iniciar_sesion') # Redirige a 'inicio' si el usuario no existe, o 'iniciar_sesion' si no ha iniciado sesión.



def agregar_infraestructura(request):
    if request.method == 'POST':  # Si el método es POST, se extraen los datos del formulario enviado.
        infraestructura = Infraestructura(
            nombre=request.POST['nombre'],
            tipo=request.POST['tipo'],
            capacidad=request.POST['capacidad'],
            descripcion=request.POST['descripcion'],
            horarios=request.POST['horarios'],
            precio=request.POST['precio'],
            foto=request.FILES['foto']
        )
        infraestructura.save()  # Guarda la infraestructura en la base de datos.
        return redirect('lista_infraestructuras')  # Redirige al usuario a la página de lista de infraestructuras.

    deportes = Deporte.objects.all()  # Obtiene los deportes para el formulario.
    # Renderiza la plantilla 'cancha/agregar_infraestructura.html'.
    # El contexto es un diccionario que le permite acceder a la variable 'deportes'.
    return render(request, 'cancha/agregar_infraestructura.html', {'deportes': deportes})

def lista_infraestructuras(request):
    infraestructuras = Infraestructura.objects.all() #  Obtiene la infraestructura por ID, o devuelve un error 404 si no se encuentra.
    return render(request, 'cancha/lista_infraestructuras.html', {'infraestructuras': infraestructuras})# Renderiza a la plantilla 'cancha/lista_infraestructuras.html' y pasa el contexto para mostrar la lista de infraestructura.

def editar_infraestructura(request, infraestructura_id):
    infraestructura = get_object_or_404(Infraestructura, id=infraestructura_id)# Obtiene el ID proporcionado de infraestructura, si no lo encuentra muestra un error de 404.
    
    if request.method == 'POST':# Si la solicitud es POST, recupera y actualiza los datos de la infraestructura con los valores enviados en el formulario.
        infraestructura.nombre = request.POST.get('nombre')
        infraestructura.descripcion = request.POST.get('descripcion')
        infraestructura.capacidad = request.POST.get('capacidad')
        infraestructura.tipo = request.POST.get('tipo')
        infraestructura.precio = request.POST.get('precio')

        if request.FILES.get('foto'):# Verificamos si se ha proporcionado una nueva foto en la solicitud.
            infraestructura.foto = request.FILES['foto']  # Actualiza la foto si se proporciona.

        infraestructura.save()  # Guarda los cambios en la base de datos.
        return redirect('lista_infraestructuras')  # Redirige a la lista de infraestructuras.

    return render(request, 'cancha/editar_infraestructura.html', {'infraestructura': infraestructura})# Renderiza a la plantilla 'cancha/editar_infraestructura.html', y le pasa el contexto.

def eliminar_infraestructura(request, infraestructura_id):
    infraestructura = get_object_or_404(Infraestructura, id=infraestructura_id)# Se obtiene el id de la infrestructura, si no la encuentra se devuelve un error 404.

    if request.method == "POST":# Si la solicitud es POST.
        infraestructura.delete()# Se procede a eliminar la infraestructura.
        return redirect('lista_infraestructuras') # Redirige a la lista de infraestructuras después de la eliminación.

    return render(request, 'cancha/eliminar_infraestructura.html', {'infraestructura': infraestructura}) #  Renderiza la plantilla para confirmar la eliminación si el método es GET.

def crear_deporte(request):
    if request.method == 'POST':# Si la solicitud es POST.
        form = DeporteForm(request.POST, request.FILES)# Se crea una instancia del formulario `DeporteForm` con los datos enviados por el usuario.
        if form.is_valid():# Si el formulario es valido
            nombre_deporte = form.cleaned_data['nombre']# Se limpia el nombre del deporte ingresado.
            
            if Deporte.objects.filter(nombre__iexact=nombre_deporte).exists():# Verificar si el deporte ya existe
                messages.error(request, 'Este deporte ya existe. Intenta con otro nombre.')# Si existe, se muestra un mensaje del error.
            else:
                form.save()# Si no existe, se guarda en la base de datos.
                messages.success(request, 'Deporte creado exitosamente.')# Se muestra un mensaje de éxito.
                return redirect('inicio')  # Redirigir al inicio después de crear el deporte
    else:# Si no es tipo POST.
        form = DeporteForm()# Se inicia un nuevo formulario vacio.
    
    return render(request, 'cancha/crear_deporte.html', {'form': form})# Renderiza la planilla 'cancha/crear_deporte.html' pasando el formulario al contexto.

# Modifica la vista para usar la relación directa con deporte
def campos_por_deporte(request, deporte_id):
    deporte = get_object_or_404(Deporte, id=deporte_id)
    
    # Filtra usando múltiples condiciones para ser más flexible
    infraestructuras = Infraestructura.objects.filter(
        Q(tipo__iexact=deporte.nombre) |  # Búsqueda exacta ignorando mayúsculas
        Q(tipo__icontains=deporte.nombre)  # Búsqueda parcial ignorando mayúsculas
    ).distinct()    
    return render(request, 'cancha/campos_por_deporte.html', {
        'deporte': deporte,
        'infraestructuras': infraestructuras
    })


def historial_reservas(request):
    usuario_id = request.session.get('usuario_id')
    
    if not usuario_id:
        messages.error(request, 'Debes iniciar sesión para ver el historial.')
        return redirect('iniciar_sesion')
    
    # Obtiene el usuario actual
    usuario = Usuario.objects.get(id=usuario_id)
    es_admin = usuario.tipo_usuario_id == 1
    
    # Filtrado inicial
    if es_admin:
        reservas = Reserva.objects.all()
    else:
        reservas = Reserva.objects.filter(usuario_id=usuario_id)
    
    # Filtrar por parámetros enviados desde el formulario
    deporte = request.GET.get('deporte')
    fecha = request.GET.get('fecha')
    usuario_nombre = request.GET.get('usuario')
    
    if deporte:
        reservas = reservas.filter(deporte__nombre__icontains=deporte)
    if fecha:
        reservas = reservas.filter(fecha=fecha)
    if usuario_nombre and es_admin:
        reservas = reservas.filter(usuario__nombre__icontains=usuario_nombre)

    paginator = Paginator(reservas, 5)
    page_number = request.GET.get('page')
    reservas_page = paginator.get_page(page_number)
    
    return render(request, 'cancha/historial.html', {
        'reservas': reservas_page,
        'usuario_id': usuario_id,
        'es_admin': es_admin,
        'fecha_actual': date.today(),
    })

def procesar_reserva(request, infraestructura_id):
    # Verifica si el usuario ha iniciado sesión
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        messages.error(request, 'Debes iniciar sesión para hacer una reserva')
        return redirect('iniciar_sesion')

    # Obtén la infraestructura
    infraestructura = get_object_or_404(Infraestructura, id=infraestructura_id)

    if request.method == 'POST':
        try:
            # Obtener el deporte asociado a la infraestructura
            deporte = get_object_or_404(Deporte, nombre=infraestructura.tipo)

            # Obtener la fecha
            fecha = datetime.strptime(request.POST.get('fecha'), '%Y-%m-%d').date()

            # Obtener la hora de inicio y asegurarse de que esté en el formato adecuado (HH:MM)
            hora = request.POST.get('hora')
            if len(hora) > 5:  # Si la cadena tiene más de 5 caracteres, eliminamos los segundos
                hora = hora[:5]
            hora_inicio = datetime.strptime(hora, '%H:%M').time()  # Convertimos a time

            # Sumar una hora a la hora de inicio para obtener la hora de fin
            hora_inicio_datetime = datetime.combine(datetime.today(), hora_inicio)  # Combina la hora con una fecha ficticia
            hora_fin_datetime = hora_inicio_datetime + timedelta(hours=1)  # Sumar 1 hora
            hora_fin = hora_fin_datetime.time()  # Obtener solo la hora

            # Validar si ya existe una reserva para la misma infraestructura, fecha y hora
            reserva_existente = Reserva.objects.filter(
                infraestructura_id=infraestructura_id,
                fecha=fecha,
                hora_inicio__lte=hora_inicio,  # Verifica si la hora_inicio es antes o igual
                hora_fin__gte=hora_inicio      # Verifica si la hora_fin es después o igual
            ).exists()

            if reserva_existente:
                messages.error(request, 'Ya existe una reserva para esta fecha y hora')
                return redirect('procesar_reserva', infraestructura_id=infraestructura_id)

            # Validar código de descuento
            codigo_descuento = request.POST.get('codigo_descuento', '').strip()
            descuento = None
            descuento_aplicado = 0

            if codigo_descuento:
                try:
                    descuento = Descuento.objects.get(codigo=codigo_descuento, activo=True)

                    # Verificar si el descuento ha expirado
                    if descuento.fecha_expiracion and descuento.fecha_expiracion < timezone.now():
                        messages.warning(request, 'El código de descuento ha expirado.')
                        descuento = None  # Invalidar el descuento y no permitir la reserva
                        return redirect('procesar_reserva', infraestructura_id=infraestructura_id)

                    # Si el código es válido y no ha expirado, se calcula el descuento
                    descuento_aplicado = infraestructura.precio * (descuento.porcentaje / 100)

                except Descuento.DoesNotExist:
                    messages.warning(request, 'El código de descuento no es válido o está inactivo.')
                    return redirect('procesar_reserva', infraestructura_id=infraestructura_id)
            # Calcular el precio total
            precio_original = infraestructura.precio
            precio_total = precio_original - descuento_aplicado

            # Crear la nueva reserva con la hora de fin calculada
            reserva = Reserva(
                usuario_id=usuario_id,
                infraestructura_id=infraestructura_id,
                fecha=fecha,
                hora_inicio=hora_inicio,
                hora_fin=hora_fin,  # Establecer la hora de fin como 1 hora más
                horario=hora_inicio,  # Asignar horario a la hora de inicio
                deporte_id=deporte.id,
                precio_total=precio_total  # Guardar el precio final en la reserva
            )

            reserva.save()

            messages.success(request, f'Reserva realizada con éxito. Total: ${precio_total:.2f}')
            return redirect('inicio')

        except Deporte.DoesNotExist:
            messages.error(request, 'El deporte especificado no existe')
            return redirect('reserva', infraestructura_id=infraestructura_id)
        except ValueError:
            messages.error(request, 'Formato de fecha u hora inválido')
            return redirect('reserva', infraestructura_id=infraestructura_id)
        except Exception as e:
            messages.error(request, f'Error al procesar la reserva: {str(e)}')
            return redirect('reserva', infraestructura_id=infraestructura_id)

    return render(request, 'cancha/reserva.html', {
        'infraestructura': infraestructura
    })

def cambiar_estado_infraestructura(request, infraestructura_id):
    if request.method == 'POST':
        infraestructura = Infraestructura.objects.get(id=infraestructura_id)
        nuevo_estado = request.POST.get('estado')
        infraestructura.estado = nuevo_estado
        infraestructura.save()
        messages.success(request, f'Estado de {infraestructura.nombre} actualizado correctamente.')
    return redirect('lista_infraestructuras')


def obtener_horas_disponibles(request, infraestructura_id):
    # Obtener la fecha enviada por el cliente
    dia = request.GET.get('dia')
    fecha = datetime.strptime(dia, '%Y-%m-%d').date()  # Convertir la fecha de string a tipo de dato date

    # Obtener la infraestructura seleccionada
    infraestructura = Infraestructura.objects.get(id=infraestructura_id)

    # Obtener todas las reservas para esa infraestructura y fecha
    reservas = Reserva.objects.filter(infraestructura=infraestructura, fecha=fecha)

    # Obtener todas las horas ocupadas en ese día
    horas_ocupadas = [reserva.horario for reserva in reservas]

    # Asumimos que la infraestructura tiene horas de disponibilidad de 8 AM a 8 PM (esto puede variar)
    horas_disponibles = []
    for hora in range(8, 21):  
        hora_inicio = f'{hora:02}:00:00'
        if hora_inicio not in horas_ocupadas:
            hora_fin = f'{hora+1:02}:00:00' 
            horas_disponibles.append({
                'hora_inicio': hora_inicio,
                'hora_fin': hora_fin
            })

    return JsonResponse({'horas_disponibles': horas_disponibles})


def editar_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)

    if request.method == 'POST':
        nueva_hora = request.POST.get('hora')  # Suponiendo que el campo de hora se pasa por POST
        # Verificar que la nueva hora esté disponible para esa infraestructura y fecha
        if nueva_hora:
            reserva.horario = nueva_hora
            reserva.save()
            messages.success(request, 'La hora de la reserva se ha modificado con éxito.')  # Mensaje de éxito
            return redirect('historial_reservas')  # Redirige al historial de reservas después de editar
        else:
            # Si la hora no está disponible o no es válida
            messages.error(request, 'Hora no válida o no disponible.')
            return redirect('editar_reserva', reserva_id=reserva.id)  # Redirige nuevamente a la página de edición

    return render(request, 'cancha/editar_reserva.html', {'reserva': reserva})

def detalle_infraestructura(request, pk):
    infraestructura = get_object_or_404(Infraestructura, pk=pk)
    return render(request, 'cancha/detalle_infraestructura.html', {'infraestructura': infraestructura})


def aplicar_descuento(codigo_descuento):
    try:
        descuento = Descuento.objects.get(codigo=codigo_descuento)

        if descuento.activo and (descuento.fecha_expiracion is None or descuento.fecha_expiracion > timezone.now()):
            return descuento
        else:

            return None
    except Descuento.DoesNotExist:
        return None

from django.contrib import admin
from django.urls import path
from cancha import views as v
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', v.inicio, name='inicio'),
    path('iniciar-sesion/', v.iniciar_sesion, name='iniciar_sesion'),
    path('cerrar-sesion/', v.cerrar_sesion, name='cerrar_sesion'),
    path('perfil/', v.perfil, name='perfil'),
    path('agregar-infraestructura/', v.agregar_infraestructura, name='agregar_infraestructura'),
    path('lista-infraestructuras/', v.lista_infraestructuras, name='lista_infraestructuras'),
    path('editar-infraestructura/<int:infraestructura_id>/', v.editar_infraestructura, name='editar_infraestructura'),
    path('eliminar-infraestructura/<int:infraestructura_id>/', v.eliminar_infraestructura, name='eliminar_infraestructura'),
    path('crear_deporte',v.crear_deporte,name='crear_deporte'),
    path('deporte/<int:deporte_id>/campos/', v.campos_por_deporte, name='campos_por_deporte'),
    path('historial-reservas/', v.historial_reservas, name='historial_reservas'),
    path('reserva/<int:infraestructura_id>/procesar/', v.procesar_reserva, name='procesar_reserva'),
    path('infraestructura/<int:infraestructura_id>/cambiar-estado/',v.cambiar_estado_infraestructura,name='cambiar_estado_infraestructura'),
    path('obtener_horas_disponibles/<int:infraestructura_id>/', v.obtener_horas_disponibles, name='obtener_horas_disponibles'),
    path('editar_reserva/<int:reserva_id>/', v.editar_reserva, name='editar_reserva'),
    path('infraestructura/<int:pk>/', v.detalle_infraestructura, name='ver_detalle_infraestructura'),
 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
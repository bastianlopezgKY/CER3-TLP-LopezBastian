from rest_framework import viewsets
from .serializer import EventoSerializer
from .models import Evento
from django.http import JsonResponse
import requests
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
import json
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseForbidden
from django.contrib.auth.models import Group



# Create your views here.

#admin

def es_administrador(user):
    return user.groups.filter(name="administrador_academico").exists()

# Decorador para proteger vistas
def admin_required(view_func):
    @login_required
    @user_passes_test(es_administrador, login_url='/login/')
    def wrapper(request, *args, **kwargs):
        return view_func(request, *args, **kwargs)
    return wrapper


#views
class EventoViewSet(viewsets.ModelViewSet):
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer

def products(request):
    # Obtener el valor del filtro desde la URL
    tipo_evento = request.GET.get('tipo_evento', '')

    # Filtrar eventos según el tipo seleccionado
    if tipo_evento:
        eventos_listados = Evento.objects.filter(tipo=tipo_evento)
    else:
        eventos_listados = Evento.objects.all()

    # Pasar los datos necesarios al template
    context = {
        "eventos": eventos_listados,
        "TIPO_EVENTO_CHOICES": Evento.TIPO_EVENTO,  # Opciones de tipos de eventos
    }

    return render(request, "products.html", context)


def gestion(request):
    EventosListados = Evento.objects.all()
#   messages.success(request, '¡Eventos listados!')
    return render(request, "gestion.html" , {"eventos": EventosListados})   

########################

def homeEvento(request):

    es_admin_academico = request.user.groups.filter(name="administrador_academico").exists()
    # Obtener el tipo de evento desde el filtro de la URL (si está presente)
    tipo_evento = request.GET.get('tipo_evento', '')

    # Filtrar eventos según el tipo, si está especificado
    if tipo_evento:
        eventos_listados = Evento.objects.filter(tipo=tipo_evento)
    else:
        eventos_listados = Evento.objects.all()  # Mostrar todos si no hay filtro

    # Pasar al contexto las opciones de tipo de evento
    data = {
        "eventos": eventos_listados,
        "TIPO_EVENTO": Evento.TIPO_EVENTO,  # Opciones para el filtro
        "filtro_tipo": tipo_evento,  # Mantener el tipo seleccionado en el template
        "es_admin_academico": es_admin_academico,  # Indicador para la plantilla
    }

    return render(request, "gestion.html", data)

#########################    

def registrarEvento(request):
    if request.method == 'POST':
        # Extraer datos del formulario usando .get para evitar errores
        nombre = request.POST.get('txtNombre', '')
        comentarios = request.POST.get('txtComentarios', '')
        fecha_inicio = request.POST.get('dateInicio', None)
        fecha_fin = request.POST.get('dateFin', None)
        tipo = request.POST.get('txtTipo', '')

        # Validación básica
        if not nombre or not fecha_inicio or not fecha_fin or not tipo:
            messages.error(request, 'Por favor, completa todos los campos obligatorios.')
            return redirect('/api/evento')  # Redirigir si faltan datos
        
        if fecha_inicio > fecha_fin:
            messages.error(request, 'La fecha de inicio no puede ser posterior a la fecha de fin.')
            return redirect('/api/evento')  # Redirigir con un mensaje de error

        # Crear el evento
        try:
            Evento.objects.create(
                nombre=nombre,
                comentarios=comentarios,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
                tipo=tipo
            )
            messages.success(request, '¡Evento registrado con éxito!')
            return redirect('/api/evento')  # Redirigir después de registrar
        except Exception as e:
            messages.error(request, f'Error al registrar el evento: {e}')
            return redirect('/api/evento')  # Redirigir si ocurre un error

    # Si no es POST, redirigir a la lista de eventos o renderizar un formulario
    messages.error(request, 'Método no permitido.')
    return redirect('/api/evento')

@admin_required
def edicionEvento(request,id):
    evento = Evento.objects.get(id=id)
    return render(request, "edicion.html", {"evento":evento})

@admin_required
def editarEvento(request):
    id=request.POST['idEvento']
    nombre=request.POST['txtNombre']
    comentarios = request.POST.get('txtComentarios', '')  # Comentarios opcionales
    fecha_inicio = request.POST['dateInicio']
    fecha_fin = request.POST['dateFin']
    tipo = request.POST['txtTipo']

    evento = Evento.objects.get(id=id)
    evento.nombre = nombre
    evento.comentarios = comentarios
    evento.fecha_inicio = fecha_inicio
    evento.fecha_fin = fecha_fin
    evento.tipo = tipo
    evento.save()
    messages.success(request, '¡Eventos editados!')
    return redirect('/api/evento')

@admin_required
def eliminarEvento(request, id):
    evento = Evento.objects.get(id=id)
    evento.delete()

    messages.success(request, '¡Evento eliminado!')

    return redirect('/api/evento')































#calendario

def calendar_view(request):
    # Obtener eventos académicos desde la base de datos
    eventos = Evento.objects.all()
    eventos_list = [
        {
            "title": evento.nombre,
            "start": evento.fecha_inicio.strftime('%Y-%m-%d'),
            "end": evento.fecha_fin.strftime('%Y-%m-%d') if evento.fecha_fin else evento.fecha_inicio.strftime('%Y-%m-%d'),
            "description": evento.comentarios,
            "type": evento.tipo
        }
        for evento in eventos
    ]

    # Obtener feriados desde la API de terceros
    url_feriados = "https://apis.digital.gob.cl/fl/feriados/2024"
    headers = {'User-Agent': 'DjangoApp (https://example.com)'}
    try:
        response = requests.get(url_feriados, headers=headers, timeout=10)
        response.raise_for_status()
        feriados_data = response.json()
        feriados_list = [
            {
                "title": feriado.get("nombre"),
                "start": feriado.get("fecha"),
                "end": feriado.get("fecha"),
                "description": "Feriado oficial",
                "type": "Feriado",
            }
            for feriado in feriados_data
        ]
    except requests.exceptions.RequestException as e:
        feriados_list = []

    # Combinar ambos tipos de eventos
    calendario = eventos_list + feriados_list

    # Pasar datos al template
    context = {
    "eventos": mark_safe(json.dumps(calendario))
}
    return render(request, 'calendario.html', context)


def cargar_datos_api_e(request):
    url = 'http://127.0.0.1:8000/api/Eventos/'
    response = requests.get(url)
    
    if response.status_code == 200:
        datos = response.json()
        for item in datos:
            Evento.objects.update_or_create(
                nombre=item.get('nombre'),
                defaults={
                    'comentarios': item.get('comentarios'),
                    'fecha_inicio': item.get('fecha_inicio'),
                    'fecha_fin': item.get('fecha_fin'),
                    'tipo': item.get('tipo'),
                }
            )
        return JsonResponse({"mensaje": "Datos api evento cargados correctamente"})
    else:
        return JsonResponse({"error": f"Error al consumir la API evento: {response.status_code}"}, status=500)

# preguntas
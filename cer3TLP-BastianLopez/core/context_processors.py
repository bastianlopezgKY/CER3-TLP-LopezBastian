from api.models import Evento

def tipos_evento(request):
    return {'TIPO_EVENTO': Evento.TIPO_EVENTO}

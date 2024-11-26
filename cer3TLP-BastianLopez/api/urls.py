from django.urls import path, include
from rest_framework import routers
from .import views
from .views import cargar_datos_api_e, registrarEvento, edicionEvento, editarEvento, eliminarEvento, homeEvento, products, gestion

router = routers.DefaultRouter()
router.register(r'Eventos', views.EventoViewSet)

urlpatterns=[
    path('', include(router.urls), name='API'),
    path('cargar_datos_e/', cargar_datos_api_e, name='cargar_datos_e'),
    path('registrarEvento/', registrarEvento),
    path('edicionEvento/<id>', edicionEvento),
    path('editarEvento/', editarEvento),
    path('eliminacionEvento/<id>', eliminarEvento),
    path('evento', homeEvento, name="evento"),
    path('products/', products, name='products'),
    path('gestion/', homeEvento, name='gestion'),
]   

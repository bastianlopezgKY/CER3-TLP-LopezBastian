from django.urls import path
from .views import home, exit, register

urlpatterns = [
    path('', home, name='home'),
#    path('products/', products, name='products'),
    path('logout/', exit, name='exit'),
    path('register/', register, name='register'),
#    path('gestion/', gestion, name='gestion'),
]

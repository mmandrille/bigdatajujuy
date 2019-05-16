from django.conf.urls import url
from django.urls import path
#Import de modulos personales
from . import views

app_name = 'calendario'
urlpatterns = [
    path('', views.calendario, name='calendario'),
    path('<str:str_fecha>', views.calendario_diario, name='calendario_diario'),
]
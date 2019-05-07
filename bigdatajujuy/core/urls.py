from django.conf.urls import url
from django.urls import path
#Import personales
from . import views

app_name = 'core'
urlpatterns = [
    #Basicas:
    url(r'^$', views.home, name='home'),
    url('^faq/$', views.faq, name='faq'),
    url('^contacto/$', views.contacto, name='contacto'),

    #Conferencia:
    path('conferencias/', views.mostrar_exposiciones, name='mostrar_exposiciones'),
    path('conferencias/add/<int:inscripto_id>/<int:inscripto_dni>', views.cargar_exposicion, name='cargar_exposicion'),
    #Expositores:
    path('expositores/', views.mostrar_expositores, name='mostrar_expositores'),
]
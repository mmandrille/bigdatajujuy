from django.conf.urls import url
from django.urls import path
#Import personales
from . import views

app_name = 'core'
urlpatterns = [
    url(r'^$', views.home, name='home'),
    
    url('^faq/$', views.faq, name='faq'),
    url('^contacto/$', views.contacto, name='contacto'),
]
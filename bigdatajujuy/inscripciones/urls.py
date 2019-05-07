from django.conf.urls import url
from django.urls import path
#Import de modulos personales
from . import views

app_name = 'inscripciones'
urlpatterns = [
    path('<str:tipo>', views.inscripcion, name='inscripcion'),

    url(r'^activate/(?P<inscripto_id>[0-9]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate'),
    url(r'^upload/csv/$', views.upload_csv_mails, name='upload_csv_mails'),

    path('listado', views.mostrar_inscriptos, name='mostrar_inscriptos'),
    path('tabla', views.mostrar_tabla_inscriptos, name='mostrar_tabla_inscriptos'),
    path('download_excel', views.descargar_inscriptos, name='descargar_inscriptos'),

    path('testmail/<int:msj_id>', views.test_mail, name='test_mail'),
    path('task_progress/<str:queue_name>', views.task_progress, name='task_progress'),
]
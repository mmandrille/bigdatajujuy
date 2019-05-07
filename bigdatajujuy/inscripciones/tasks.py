#Traemos el sistema de Backgrounds
from background_task import background
from django.core import mail
from django.template.loader import render_to_string
from bigdatajujuy.settings import EMAIL_HOST_USER

#Import Personales
from .models import Mails, Mensajes, Progress_Links
from .functions import delete_tags

#Rutinas Base:
def crear_progress_link(new_queue):
    print("Se creo link a: " + new_queue)
    p = Progress_Links()
    p.tarea = new_queue
    p.progress_url = '/inscribir/task_progress/' + new_queue
    p.save()
    return new_queue

#Tareas
@background(schedule=60)
def crear_mails(lista_mails):
    crear_mails = list()
    for mail in lista_mails:
        crear_mails.append(Mails(email=str(mail)))
    Mails.objects.bulk_create(crear_mails)

@background(schedule=60)
def enviar_mails(msj_id, lista_mails):
    #Obtenemos el mensaje:
    mensaje = Mensajes.objects.get(pk=msj_id)
    #Abrimos el envio de correos
    connection = mail.get_connection()
    connection.open()
    #Instanciamos el objeto email
    msj_simple = delete_tags(mensaje.cuerpo)
    email = mail.EmailMultiAlternatives(mensaje.titulo, msj_simple, EMAIL_HOST_USER,
                          bcc=lista_mails, connection=connection)
    msj_html = render_to_string('email_base.html', {
                'mensaje': mensaje,
                })
    email.attach_alternative(msj_html, "text/html")
    #Lo mandamos
    email.send()
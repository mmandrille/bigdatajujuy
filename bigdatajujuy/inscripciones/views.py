from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
#Import Particulares
import csv

#Task Manager Models
from background_task.models import Task as bg_Tasks
from background_task.models_completed import CompletedTask as bg_CompletedTask
#decoradores
from django.contrib.admin.views.decorators import staff_member_required

#Import Personales
from .models import Inscripto, Mensajes
from .modelforms import InscriptoForm_asistente, InscriptoForm_expositor
from .tokens import account_activation_token
from .tasks import crear_mails, crear_progress_link

def inscripcion(request):
    tipo = request.path[11:]
    if request.method == 'POST':#Si intenta inscribirse
        if tipo == 'expositor':#Cargamos el objecto form segun tipo de inscripcion
            form = InscriptoForm_expositor(request.POST)
        else: form = InscriptoForm_asistente(request.POST)
        
        if form.is_valid():#Si el formulario se completo correctamente
            to_email = form.cleaned_data.get('email')#Obtenemos el correo
        
            try: inscripto = Inscripto.objects.get(email=to_email) #Chequeamos si no esta inscripto    
            except Inscripto.DoesNotExist:#Si no existe
                inscripto = form.save()#Creamos el inscripto
        
            if not inscripto.activo:#Si el usuario aun no fue activado le vamos a enviar un mail de validacion
                mail_subject = 'Confirma tu Inscripcion a Big Data Jujuy.'
                #Definimos el tipo de mail a enviar
                if tipo == 'expositor': mail_template= 'acc_active_email_exp.html'
                else: mail_template= 'acc_active_email.html'
                #Preparamos el correo electronico
                message = render_to_string(mail_template, {
                    'inscripto': inscripto,
                    'token':account_activation_token.make_token(inscripto),
                })
                #Instanciamos el objeto mail con destinatario
                email = EmailMessage(
                            mail_subject, message, to=[to_email]
                )
                #Enviamos el correo
                email.send()
                #Informamos que el mail fue enviado
                return render(request, 'resultado.html', {'texto': 'Por Favor Confirme la creacion de su cuenta en el correo que recibio', })
            else:
                #informamos que la cuenta ya fue activada.
                return render(request, 'resultado.html', {'texto': 'El mail informado ya fue validado en otra inscripcion', })
            if tipo == 'expositor': inscripto.categoria = 2
            inscripto.save()
    else:#En caso de que ingrese para registrarse
        if tipo == 'expositor': form = InscriptoForm_expositor(initial={'categoria':2,})
        else: form = InscriptoForm_asistente()
    return render(request, 'inscripcion.html', {'form': form, })

def activate(request, inscripto_id, token):
    try:
        inscripto = Inscripto.objects.get(pk=inscripto_id)
    except(TypeError, ValueError, OverflowError, Inscripto.DoesNotExist):
        inscripto = None
    if inscripto is not None and account_activation_token.check_token(inscripto, token):
        inscripto.activo = True
        inscripto.save()
        return render(request, 'resultado.html', {'texto': 'Excelente! Su inscripcion fue validada.', })
    else:
        return render(request, 'resultado.html', {'texto': 'El link de activacion es invalido!', })

def test_mail(request, msj_id):
    mail = Mensajes.objects.get(pk=msj_id)
    return render(request, 'email_base.html', {'mensaje': mail, })

@staff_member_required
def mostrar_inscriptos(request):
    tipo_usuario = [True, False]
    inscriptos = Inscripto.objects.all().order_by('-apellido')
    return render(request, 'inscriptos.html', {'inscriptos': inscriptos, 'tipo_usuario': tipo_usuario })

@staff_member_required
def mostrar_tabla_inscriptos(request):
    tipo_usuario = [True, False]
    inscriptos = Inscripto.objects.all().order_by('-apellido')
    return render(request, 'inscriptos_tabla.html', {'inscriptos': inscriptos, 'tipo_usuario': tipo_usuario })

@staff_member_required
def descargar_inscriptos(request):
    #Obtenemos todos los inscriptos
    inscriptos = Inscripto.objects.all().order_by('-apellido')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="listado_inscriptos.csv"'
    writer = csv.writer(response)
    writer.writerow(['Apellido', 'Nombre','Dni', 'Telefono', 'Correo Electronico', 'Validado'])
    for inscripto in inscriptos:
        writer.writerow([inscripto.apellido, inscripto.nombres, inscripto.num_doc, inscripto.telefono, inscripto.email, inscripto.activo])
    return response

# Create your views here.
@staff_member_required
def upload_csv_mails(request):
    count = 0
    data = {}
    if "GET" == request.method:
        return render(request, "upload_csv.html", data)
    # if not GET, then proceed
    csv_file = request.FILES["csv_file"]
    if not csv_file.name.endswith('.csv'):
        messages.error(request,'File is not CSV type')
        return HttpResponseRedirect(reverse("inscripciones:upload_csv"))
        #if file is too large, return
    if csv_file.multiple_chunks():
        messages.error(request,"Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
        return HttpResponseRedirect(reverse("inscripciones:upload_csv"))
        
    file_data = csv_file.read().decode("utf-8")
    lines = file_data.split("\n")
    #loop over the lines and save them in db. If error , store as string and then display
    #llamar funcion cada 100 mails.
    count = 0
    new_queue = crear_progress_link("CrearMails:"+str(datetime.now()).replace(" ", ">")[0:16])
    while (count + 100) < len(lines):
        crear_mails(lines[count:count+100], schedule=int(count/10), queue=new_queue)
        count+=100
    crear_mails(lines[count:len(lines)], schedule=int(count/10), queue=new_queue)
    return render(request, 'upload_csv.html', {'count': len(lines), 'new_queue': new_queue })

def task_progress(request, queue_name):
    tareas_en_progreso = bg_Tasks.objects.filter(queue= queue_name)
    tareas_terminadas = bg_CompletedTask.objects.filter(queue= queue_name)
    return render(request, 'task_progress.html', {'tarea_queue': queue_name, 
                                                'tareas_totales': (len(tareas_en_progreso)+len(tareas_terminadas)) ,
                                                'tareas_en_cola': len(tareas_en_progreso), 
                                                'tareas_terminadas': len(tareas_terminadas),
                                                "refresh": True })
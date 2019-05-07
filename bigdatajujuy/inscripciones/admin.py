from django.contrib import admin
from django.contrib.auth.models import User

#Import Personales
from .tasks import enviar_mails, crear_progress_link
from .models import Inscriptos, Mensajes, Mails, Progress_Links

#Definimos acciones extras:
def enviar_mail(modeladmin, request, queryset):    
    #Conseguimos la lista de destinatarios
    for obj in queryset:
        mail_list = list()
        if obj.destinatarios == 0:
            mail_list = [obj.autor.email]
        elif obj.destinatarios == 1:
            for u in User.objects.all(): mail_list.append(u.email)
        elif obj.destinatarios == 2:
            for u in Inscriptos.objects.all(): mail_list.append(u.email)
        elif obj.destinatarios == 3:
            for u in Mails.objects.filter(valido=True): mail_list.append(u.email)
        elif obj.destinatarios == 4:
            for u in Mails.objects.all(): mail_list.append(u.email)
        #empezamos a bulkear y creamos las background tasks!
        count = 0
        new_queue =  crear_progress_link(str("EnviarMails:"+str(obj.id)))
        while (count + obj.cantidad) < len(mail_list):
            enviar_mails(msj_id=obj.id, lista_mails=mail_list[count:(count+obj.cantidad)], schedule=int(count/10), queue=new_queue)
            count+= obj.cantidad
        enviar_mails(msj_id=obj.id, lista_mails=mail_list[count:len(mail_list)], schedule=int(count/10), queue=new_queue)
        obj.enviado = True
        obj.save()

#Le damos mejores descripciones a las Acciones
enviar_mail.short_description = "Comenzar el envio Masivo"

#Definimos expansiones
class MensajesAdmin(admin.ModelAdmin):
    list_display = ['nombre','destinatarios', 'enviado']
    ordering = ['nombre']
    actions = [enviar_mail]

class InscriptosAdmin(admin.ModelAdmin):
    list_filter = ['activo', 'categoria']

# Register your models here.
admin.site.register(Inscriptos, InscriptosAdmin)
admin.site.register(Mensajes, MensajesAdmin)
admin.site.register(Mails)
admin.site.register(Progress_Links)

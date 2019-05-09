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
        cargar_destinatarios = [lambda:mail_list.append(obj.autor.email), 
                                lambda:[mail_list.append(u.email) for u in User.objects.all()], 
                                lambda:[mail_list.append(u.email) for u in Inscriptos.objects.all()],
                                lambda:[mail_list.append(u.email) for u in Mails.objects.filter(valido=True)],
                                lambda:[mail_list.append(u.email) for u in Mails.objects.all()]]
        cargar_destinatarios[obj.destinatarios]()
        #empezamos a bulkear y creamos las background tasks!
        count = 0
        new_queue =  crear_progress_link(str("EnviarMails:"+str(obj.id)))
        while (count + obj.cantidad) < len(mail_list):
            enviar_mails(msj_id=obj.id, lista_mails=mail_list[count:(count+obj.cantidad)], schedule=int(count/10), queue=new_queue)
            count+= obj.cantidad
        enviar_mails(msj_id=obj.id, lista_mails=mail_list[count:len(mail_list)], schedule=int(count/10), queue=new_queue)
        obj.enviado = True
        obj.save()

def remove_from_fieldsets(fieldsets, fields):
    for fieldset in fieldsets:
        for field in fields:
            if field in fieldset[1]['fields']:
                new_fields = []
                for new_field in fieldset[1]['fields']:
                    if not new_field in fields:
                        new_fields.append(new_field)
                        
                fieldset[1]['fields'] = tuple(new_fields)
                break


#Le damos mejores descripciones a las Acciones
enviar_mail.short_description = "Comenzar el envio Masivo"

#Definimos expansiones
class MensajesAdmin(admin.ModelAdmin):
    list_display = ['nombre','destinatarios', 'enviado']
    ordering = ['nombre']
    actions = [enviar_mail]

class InscriptosAdmin(admin.ModelAdmin):
    list_filter = ['activo', 'categoria', 'autorizado']
    def get_fieldsets(self, request, obj=None):
        fieldsets = super(InscriptosAdmin, self).get_fieldsets(request, obj)
        if obj.categoria == 1: remove_from_fieldsets(fieldsets, ('autorizado',))
        return fieldsets

# Register your models here.
admin.site.register(Inscriptos, InscriptosAdmin)
admin.site.register(Mensajes, MensajesAdmin)
admin.site.register(Mails)
admin.site.register(Progress_Links)

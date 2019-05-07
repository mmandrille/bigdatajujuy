from django.contrib import admin
from .models import Evento
# Register your models here.
class EventoAdmin(admin.ModelAdmin):
    list_filter = ['importante']

#Los mandamos al admin
admin.site.register(Evento, EventoAdmin)

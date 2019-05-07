from django.contrib import admin

#Incluimos modelos
from .models import Faq, Conferencias
from inscripciones.models import Inscriptos

#Realizamos modificaciones sobre los modelos
class ConferenciasAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "expositor":
            kwargs["queryset"] = Inscriptos.objects.filter(categoria=2)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# Register your models here.
admin.site.register(Faq)
admin.site.register(Conferencias, ConferenciasAdmin)
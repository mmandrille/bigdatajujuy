from django.contrib import admin

#Incluimos modelos
from .models import Faq, Conferencia
from inscripciones.models import Inscripto

#Realizamos modificaciones sobre los modelos
class ConferenciaAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "expositor":
            kwargs["queryset"] = Inscripto.objects.filter(categoria=2, autorizado=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    list_filter = ['autorizada']


# Register your models here.
admin.site.register(Faq)
admin.site.register(Conferencia, ConferenciaAdmin)
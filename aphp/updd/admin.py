from django.contrib import admin
from .models import *
from django.contrib import admin

class PersonnelAdmin(admin.ModelAdmin):
     model= Personnel
     filter_horizontal = ('dossiermedical',)


# Register your models here.
admin.site.register(Structure)
admin.site.register(Hopital)
admin.site.register(Pole)
admin.site.register(Service)
admin.site.register(UH)
admin.site.register(US)
admin.site.register(Personnel, PersonnelAdmin)
admin.site.register(Medecin)
admin.site.register(Infirmier)
admin.site.register(Secretaire)
admin.site.register(Patient)
admin.site.register(DossierMedical)
admin.site.register(Document)
admin.site.register(Diagnostic)
admin.site.register(Soin)
admin.site.register(Ordonnance)
admin.site.register(Operation)
admin.site.register(Message)
admin.site.register(Notification)

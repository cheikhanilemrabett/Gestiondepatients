from django.contrib import admin
from .models import  *
# Register your models here.



# Enregistrement des modèles dans l'interface d'administration
admin.site.register(Department)
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Appointment)
admin.site.register(RevealRecords)

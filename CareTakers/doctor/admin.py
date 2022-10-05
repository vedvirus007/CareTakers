from django.contrib import admin
from .models import Appointment,clinic,Prediction, patient
# Register your models here.

admin.site.register(Appointment)
admin.site.register(clinic)
admin.site.register(Prediction)
admin.site.register(patient)

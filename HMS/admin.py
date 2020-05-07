from django.contrib import admin
from HMS.models import *
# Register your models here.
admin.site.register(patient)
admin.site.register(physician)
admin.site.register(prescription)
admin.site.register(report)
admin.site.register(nurse)
admin.site.register(surgeon)
admin.site.register(ward)

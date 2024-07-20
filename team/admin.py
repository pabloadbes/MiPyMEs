from django.contrib import admin
from .models import Supervisor, Surveyor

# Register your models here.
class SupervisorAdmin(admin.ModelAdmin):
   list_display = ('user', 'SUP_CODE')

class SurveyorAdmin(admin.ModelAdmin):
   list_display = ('user', 'ENC_CODE', 'supervisor')

admin.site.register(Supervisor, SupervisorAdmin)
admin.site.register(Surveyor, SurveyorAdmin)

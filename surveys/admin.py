from django.contrib import admin
from .models import Survey

# Register your models here.
class SurveyAdmin(admin.ModelAdmin):
    list_display = ('company', 'updated')

admin.site.register(Survey, SurveyAdmin)

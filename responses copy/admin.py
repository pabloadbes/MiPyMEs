from django.contrib import admin
from .models import Response

# Register your models here.
class ResponseAdmin(admin.ModelAdmin):
    list_display = ('company', 'option')

admin.site.register(Response, ResponseAdmin)

from django.contrib import admin
from .models import  UnderWriter



    
@admin.register(UnderWriter)
class UnderWriterAdmin(admin.ModelAdmin):
    list_display = ['name', 'member']
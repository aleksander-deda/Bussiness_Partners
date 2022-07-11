from django.contrib import admin

from easypays.models import SuperEasyPay


@admin.register(SuperEasyPay)
class SuperEasyPayAdmin(admin.ModelAdmin):
    list_display = ['name', 'member']

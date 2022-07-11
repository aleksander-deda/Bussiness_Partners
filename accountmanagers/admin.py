from django.contrib import admin

from .models import AccountManager


@admin.register(AccountManager)
class AccountManagerAdmin(admin.ModelAdmin):
    list_display = ['name', 'member']



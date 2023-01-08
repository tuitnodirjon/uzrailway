from django.contrib import admin
from .models import TgUser


@admin.register(TgUser)
class TgUserAdmin(admin.ModelAdmin):
    list_display = ('tg_id', 'username', 'first_name', 'last_name', 'phone_number', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('tg_id', 'username', 'first_name', 'last_name', 'phone_number')
    list_per_page = 20

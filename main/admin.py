from django.contrib import admin
from .models import Station, UserPassword, Notifications, TgUser


@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    list_display = ['id', 'name_uz', 'name_en', 'name_ru', 'code']
    search_fields = ['name_uz', 'name_ru', 'name_en', 'code']
    list_filter = ['is_uzbek']


@admin.register(TgUser)
class TgUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'first_name', 'last_name']
    search_fields = ['username', 'first_name', 'last_name']


@admin.register(UserPassword)
class UserPasswordAdmin(admin.ModelAdmin):
    list_display = ['login', 'password', 'created_at']
    search_fields = ['login']


@admin.register(Notifications)
class NotificationsAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'station_from', 'station_to', 'date', 'is_active']
    search_fields = ['user__first_name', 'user_last__name']
    autocomplete_fields = ['station_from', 'station_to', 'user']

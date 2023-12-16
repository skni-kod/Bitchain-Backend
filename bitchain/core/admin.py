from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _
from core import models


class UserAdmin(BaseUserAdmin):
    """User admin class"""
    ordering = ['id']
    list_display = ['email', 'full_name', 'nick_name', 'date_of_birth_format', 'pesel', 'account_balance', 'image']

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'nick_name', 'date_of_birth', 'pesel', 'password1', 'password2', 'image'),
        }),
    )
    fieldsets = (
        (None, {'fields': ('password', )}),
        (_('Personal info'), {'fields': ('full_name', 'nick_name', 'date_of_birth',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',)}),
        (_('Important dates'), {'fields': ('last_login', )}),
    )
    readonly_fields = ('last_login',)

    def date_of_birth_format(self, obj):
        return obj.date_of_birth.strftime("%Y-%m-%d")
    date_of_birth_format.short_description = 'Date of birth'


admin.site.register(models.User, UserAdmin)

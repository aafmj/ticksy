from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

from .models import User, Identity


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active')
    search_fields = ['email', 'first_name', 'last_name']
    readonly_fields = ('date_joined', 'last_login')
    fieldsets = (
        (None, {'fields': ('email', 'first_name', 'last_name', 'avatar', 'code', 'password', 'is_active')}),
        (_('important dates'), {'fields': ('date_joined', 'last_login')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'avatar', 'code'),
        }),
    )


class IdentityAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'request_time', 'expire_time')
    list_filter = ['status', 'request_time', 'expire_time']
    search_fields = ['user', 'email']


admin.site.register(User, UserAdmin)
admin.site.register(Identity, IdentityAdmin)

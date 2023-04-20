"""
Django admin customization.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from core import models


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""
    ordering = ["id"]
    list_display = ["id", "phone_number", "chat_type", "module"]
    fieldsets = (
        (None, {"fields": (
            "phone_number",
            "password",
            "chat_type",
            "module"
        )}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                )
            }
        ),
        (_("Important dates"), {"fields": ("last_login",)})
    )
    readonly_fields = ["last_login"]
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "phone_number",
                "password1",
                "password2",
                "chat_type",
                "module",
                "is_active",
                "is_staff",
                "is_superuser"
            )
        }),
    )


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Session)

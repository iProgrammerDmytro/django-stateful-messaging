"""
Database models
"""
from django.conf import settings
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.constants import ChatType, Module


class UserManager(BaseUserManager):
    """Manager for users."""
    def _validate_phone_number(self, phone_number: str, chat_type: str) -> str:
        plus_is_missed = not phone_number.startswith("+")

        if plus_is_missed:
            phone_number = "+" + phone_number

        if chat_type is not None:
            if chat_type == ChatType.DEFAULT.value:
                plus_index = phone_number.index("+")
                return phone_number[plus_index:]
            return "whatsapp:" + phone_number

        return phone_number

    def create_user(self, phone_number, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not phone_number:
            raise ValueError("User must have the phone number.")
        phone_number = self._validate_phone_number(
            phone_number,
            extra_fields.get("chat_type")
        )
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(settings.DEFAULT_PASSWORD)
        user.save(using=self._db)

        return user

    def create_superuser(self, phone_number, password):
        """Create and return a new superuser."""
        user = self.create_user(phone_number)
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    phone_number = models.CharField(max_length=128, unique=True)
    chat_type = models.CharField(
        max_length=24,
        choices=[(chat_type.value, chat_type.value) for chat_type in ChatType],
        default=ChatType.DEFAULT.value,
    )
    module = models.CharField(
        max_length=24,
        choices=[(module.value, module.value) for module in Module],
        default=Module.BGCHECK.value
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    name = models.CharField(
        max_length=64,
        null=True,
        blank=True
    )

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'


class Session(models.Model):
    """
    Chat with the user according to his module/algorithm.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    created = models.DateTimeField(
        auto_now=False,
        auto_now_add=True,
        help_text=_("Date and time when the session was created.")
    )
    end_date = models.DateTimeField(
        auto_now=False,
        auto_now_add=False,
        help_text=_("Date and time when session was ended."),
        blank=True,
        null=True
    )
    active = models.BooleanField(default=False)
    state = models.BinaryField(blank=True, null=True)
    last_user_bgcheck_value = models.SmallIntegerField(
        blank=True,
        null=True
    )
    stop_session_flag = models.SmallIntegerField(
        blank=True,
        null=True,
        help_text=_("Signal for system that session should be stopped.")
    )

    def __str__(self):
        return f"Session {self.id} with {self.user.phone_number}"

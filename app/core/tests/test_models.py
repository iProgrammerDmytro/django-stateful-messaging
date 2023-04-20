"""
Tests for models.
"""
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase

from core.constants import ChatType


class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_phone_number_successful(self):
        """Test creating a user with the phone number is successful."""
        phone_number = "+380632284494"
        user = get_user_model().objects.create_user(
            phone_number=phone_number
        )

        self.assertEqual(user.phone_number, phone_number)
        self.assertTrue(user.check_password(settings.DEFAULT_PASSWORD))

    def test_new_user_phone_number_normalized(self):
        """Test phone number is normalized for new users."""
        phone_number = "380632284494"
        expected = "+380632284494"

        user = get_user_model().objects.create_user(phone_number)
        self.assertEqual(user.phone_number, expected)

    def test_new_user_without_phone_number_raises_error(self):
        """
        Test creating a user without phone number
        raises a ValueError.
        """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user("")

    def create_super_user(self):
        """Test creating a superuser."""
        user = get_user_model().objects.create_superuser(
            "+380451299203"
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_default_chat_type(self):
        """
        Test creating a user with default chat type
        creates no prefix for the phone number.
        """
        user = get_user_model().objects.create(phone_number="+381232132121313")
        phone_number = user.phone_number
        plus_index = phone_number.index("+")

        self.assertEqual(phone_number, phone_number[plus_index:])

    def test_whatsapp_chat_type(self):
        """
        Test creating a user with whatsapp chat type
        creates whatsapp prefix for the phone number.
        """
        phone_number = "+1231321321312"
        whatsapp_user = get_user_model().objects.create_user(
            phone_number=phone_number,
            chat_type=ChatType.WHATS_APP.value
        )
        exptected_number = "whatsapp:" + phone_number

        self.assertEqual(whatsapp_user.phone_number, exptected_number)

import os

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.conf import settings
from core.models import FavoriteUserCryptocurrency

USER_EXAMPLE = {
    'email': 'test@example.com',
    'password': 'testing123',
    'full_name': 'Test User',
    'nick_name': 'Test',
    'date_of_birth': '1990-01-01',
    'pesel': '90010100000',
}

class UserModelTestCase(TestCase):
    """Test models"""



    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""

        user = get_user_model().objects.create_user(
            email=USER_EXAMPLE['email'],
            password=USER_EXAMPLE['password'],
            full_name=USER_EXAMPLE['full_name'],
            nick_name=USER_EXAMPLE['nick_name'],
            date_of_birth=USER_EXAMPLE['date_of_birth'],
            pesel=USER_EXAMPLE['pesel'],
        )
        self.assertEqual(user.email, USER_EXAMPLE['email'])
        self.assertTrue(user.check_password(USER_EXAMPLE['password']))
        self.assertEqual(user.full_name, USER_EXAMPLE['full_name'])
        self.assertEqual(user.nick_name, USER_EXAMPLE['nick_name'])
        self.assertEqual(user.date_of_birth, USER_EXAMPLE['date_of_birth'])
        self.assertEqual(user.pesel, USER_EXAMPLE['pesel'])

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        sample_email = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TeSt3@EXAMPLE.cOm', 'TeSt3@example.com'],
            ['TEST4@EXAMPLE.COM', 'TEST4@example.com'],
        ]
        for entry_email, expected_email in sample_email:
            user = get_user_model().objects.create_user(
                email=entry_email,
                password=USER_EXAMPLE['password'],
                full_name=USER_EXAMPLE['full_name'],
                nick_name=USER_EXAMPLE['nick_name'],
                date_of_birth=USER_EXAMPLE['date_of_birth'],
                pesel=USER_EXAMPLE['pesel'],
            )
            self.assertEqual(user.email, expected_email)
            user.delete()

    def test_new_user_without_email_raises_error(self):
        """Test creating user without email raises error"""
        with self.assertRaises(ValueError):
            user = get_user_model().objects.create_user(
                email=None,
                password=USER_EXAMPLE['password'],
                full_name=USER_EXAMPLE['full_name'],
                nick_name=USER_EXAMPLE['nick_name'],
                date_of_birth=USER_EXAMPLE['date_of_birth'],
                pesel=USER_EXAMPLE['pesel'],
            )

    def test_new_user_without_full_name_raises_error(self):
        """Test creating user without full_name raises error"""
        with self.assertRaises(ValueError):
            user = get_user_model().objects.create_user(
                email=USER_EXAMPLE['email'],
                password=USER_EXAMPLE['password'],
                full_name=None,
                nick_name=USER_EXAMPLE['nick_name'],
                date_of_birth=USER_EXAMPLE['date_of_birth'],
                pesel=USER_EXAMPLE['pesel'],
            )

    def test_new_user_without_nick_name_raises_error(self):
        """Test creating user without nick_name raises error"""
        with self.assertRaises(ValueError):
            user = get_user_model().objects.create_user(
                email=USER_EXAMPLE['email'],
                password=USER_EXAMPLE['password'],
                full_name=USER_EXAMPLE['full_name'],
                nick_name=None,
                date_of_birth=USER_EXAMPLE['date_of_birth'],
                pesel=USER_EXAMPLE['pesel'],
            )

    def test_new_user_without_date_of_birth_raises_error(self):
        """Test creating user without date_of_birth raises error"""
        with self.assertRaises(ValueError):
            user = get_user_model().objects.create_user(
                email=USER_EXAMPLE['email'],
                password=USER_EXAMPLE['password'],
                full_name=USER_EXAMPLE['full_name'],
                nick_name=USER_EXAMPLE['nick_name'],
                date_of_birth=None,
                pesel=USER_EXAMPLE['pesel'],
            )

    def test_new_user_without_pesel_raises_error(self):
        """Test creating user without pesel raises error"""
        with self.assertRaises(ValueError):
            user = get_user_model().objects.create_user(
                email=USER_EXAMPLE['email'],
                password=USER_EXAMPLE['password'],
                full_name=USER_EXAMPLE['full_name'],
                nick_name=USER_EXAMPLE['nick_name'],
                date_of_birth=USER_EXAMPLE['date_of_birth'],
                pesel=None,
            )

    def test_create_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            email=USER_EXAMPLE['email'],
            password=USER_EXAMPLE['password'],
            full_name=USER_EXAMPLE['full_name'],
            nick_name=USER_EXAMPLE['nick_name'],
            date_of_birth=USER_EXAMPLE['date_of_birth'],
            pesel=USER_EXAMPLE['pesel'],
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)


class DefaultImageTestCase(TestCase):
    def test_default_image_exists(self):
        """Test if default.jpg exists in the media directory"""

        absolute_path = os.path.abspath(os.path.join('..', settings.MEDIA_ROOT, settings.DEFAULT_AVATAR_PATH))
        file_exists = os.path.isfile(absolute_path)

        self.assertTrue(file_exists)
        
class FavoriteUserCryptocurrencyModelTestCase(TestCase):
    

    def test_unique_favorite_user_cryptocurrency(self):
        user = get_user_model().objects.create_user(
                email=USER_EXAMPLE['email'],
                password=USER_EXAMPLE['password'],
                full_name=USER_EXAMPLE['full_name'],
                nick_name=USER_EXAMPLE['nick_name'],
                date_of_birth=USER_EXAMPLE['date_of_birth'],
                pesel=USER_EXAMPLE['pesel'],
                )
        # Creating two FavoriteUserCryptocurrency objects with the same user but different cryptocurrencies
        favorite1 = FavoriteUserCryptocurrency.objects.create(user=user, cryptocurrency_symbol='BTC')
        favorite2 = FavoriteUserCryptocurrency.objects.create(user=user, cryptocurrency_symbol='ETH')

        # Checking if the objects are created correctly
        self.assertEqual(favorite1.user, user)
        self.assertEqual(favorite1.cryptocurrency_symbol, 'BTC')
        self.assertEqual(favorite2.user, user)
        self.assertEqual(favorite2.cryptocurrency_symbol, 'ETH')

        # Attempting to create a second object with the same user and the same cryptocurrency should result in an error
        with self.assertRaises(Exception):
            FavoriteUserCryptocurrency.objects.create(user=user, cryptocurrency_symbol='BTC')
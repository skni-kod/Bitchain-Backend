from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    """Test models"""

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'test@example.com'
        password = 'testing123'
        full_name = 'Test User'
        nick_name = 'Test'
        date_of_birth = '1990-01-01'
        pesel = '90010100000'

        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            full_name=full_name,
            nick_name=nick_name,
            date_of_birth=date_of_birth,
            pesel=pesel,
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertEqual(user.full_name, full_name)
        self.assertEqual(user.nick_name, nick_name)
        self.assertEqual(user.date_of_birth, date_of_birth)
        self.assertEqual(user.pesel, pesel)

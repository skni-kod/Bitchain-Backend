from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    """Test models"""

    email_example = 'test@example.com'
    password_example = 'testing123'
    full_name_example = 'Test User'
    nick_name_example = 'Test'
    date_of_birth_example = '1990-01-01'
    pesel_example = '90010100000'

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""

        user = get_user_model().objects.create_user(
            email=self.email_example,
            password=self.password_example,
            full_name=self.full_name_example,
            nick_name=self.nick_name_example,
            date_of_birth=self.date_of_birth_example,
            pesel=self.pesel_example,
        )
        self.assertEqual(user.email, self.email_example)
        self.assertTrue(user.check_password(self.password_example))
        self.assertEqual(user.full_name, self.full_name_example)
        self.assertEqual(user.nick_name, self.nick_name_example)
        self.assertEqual(user.date_of_birth, self.date_of_birth_example)
        self.assertEqual(user.pesel, self.pesel_example)

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        sample_email = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TeSt3@EXAMPLE.cOm', 'TeSt3@example.com'],
            ['TEST4@EXAMPLE.COM', 'TEST4@example.com'],
        ]
        for entry_email, expected_email in sample_email:
            user = get_user_model().objects.create_user(email=entry_email, password=self.password_example,
                                                        full_name=self.full_name_example,
                                                        nick_name=self.nick_name_example,
                                                        date_of_birth=self.date_of_birth_example,
                                                        pesel=self.pesel_example)
            self.assertEqual(user.email, expected_email)
            user.delete()

    def test_new_user_without_email_raises_error(self):
        """Test creating user without email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email=None, password=self.password_example,
                                                 full_name=self.full_name_example,
                                                 nick_name=self.nick_name_example,
                                                 date_of_birth=self.date_of_birth_example,
                                                 pesel=self.pesel_example)

    def test_new_user_without_full_name_raises_error(self):
        """Test creating user without full_name raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email=self.email_example, password=self.password_example,
                                                 full_name=None,
                                                 nick_name=self.nick_name_example,
                                                 date_of_birth=self.date_of_birth_example,
                                                 pesel=self.pesel_example)

    def test_new_user_without_nick_name_raises_error(self):
        """Test creating user without nick_name raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email=self.email_example, password=self.password_example,
                                                 full_name=self.full_name_example,
                                                 nick_name=None,
                                                 date_of_birth=self.date_of_birth_example,
                                                 pesel=self.pesel_example)

    def test_new_user_without_date_of_birth_raises_error(self):
        """Test creating user without date_of_birth raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email=self.email_example, password=self.password_example,
                                                 full_name=self.full_name_example,
                                                 nick_name=self.nick_name_example,
                                                 date_of_birth=None,
                                                 pesel=self.pesel_example)

    def test_new_user_without_pesel_raises_error(self):
        """Test creating user without pesel raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email=self.email_example, password=self.password_example,
                                                 full_name=self.full_name_example,
                                                 nick_name=self.nick_name_example,
                                                 date_of_birth=self.date_of_birth_example,
                                                 pesel=None)

    def test_create_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            email=self.email_example,
            password=self.password_example,
            full_name=self.full_name_example,
            nick_name=self.nick_name_example,
            date_of_birth=self.date_of_birth_example,
            pesel=self.pesel_example,
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

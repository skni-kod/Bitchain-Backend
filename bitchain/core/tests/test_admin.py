"""
Tests for the admin panel
"""
from django.test import (
    TestCase, Client
)
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):
    """Test admin site"""

    def setUp(self):
        """Setup function"""
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@example.com',  # email must be unique
            password='testing123',
            full_name='Test Admin',
            nick_name='TestAdmin',  # nick_name must be unique
            date_of_birth='1990-01-01',
            pesel='90010100000', 
            )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='user@example.com',  # email must be unique
            password='testing123',
            full_name='Test User',
            nick_name='TestUser',  # nick_name must be unique
            date_of_birth='1991-02-01',
            pesel='90010100001', 
            )

    def test_users_listed(self):
        """Test that users are listed on user page"""
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)  # res = response

        self.assertContains(res, self.user.full_name)
        self.assertContains(res, self.user.nick_name)
        self.assertContains(res, self.user.email)
        self.assertContains(res, self.user.date_of_birth)
        self.assertContains(res, self.user.pesel)
        self.assertContains(res, self.user.image)

    def test_edit_user_page(self):
        """Test that the user edit page works"""
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test that the create user page works"""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)


class UserManager(BaseUserManager):
    """Custom user manager"""

    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # encrypts password
        user.save(using=self._db)  # standard procedure for saving objects in django project
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True, editable=False)
    full_name = models.CharField(max_length=255)
    nick_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    pesel = models.CharField(max_length=11, unique=True, editable=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()  # assigns custom user manager to objects attribute

    USERNAME_FIELD = 'email'  # default is username
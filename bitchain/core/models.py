from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)


class UserManager(BaseUserManager):
    """Custom user manager"""

    def create_user(self, email, password, full_name, nick_name, date_of_birth, pesel,  **extra_fields):
        """Creates and saves a new user"""

        if not email:
            raise ValueError('User must have an email address')
        if not password:
            raise ValueError('User must have a password')
        if not full_name:
            raise ValueError('User must have a full name')
        if not nick_name:
            raise ValueError('User must have a nick name')
        if not date_of_birth:
            raise ValueError('User must have a date of birth')
        if not pesel:
            raise ValueError('User must have a pesel')

        user = self.model(email=self.normalize_email(email), full_name=full_name, nick_name=nick_name,
                          date_of_birth=date_of_birth, pesel=pesel, **extra_fields)
        user.set_password(password)  # encrypts password
        user.save(using=self._db)  # standard procedure for saving objects in django project
        return user

    def create_superuser(self, email, password, full_name, nick_name, date_of_birth, pesel, **extra_fields):
        """Creates and saves a new superuser"""
        user = self.create_user(email, password, full_name, nick_name, date_of_birth, pesel, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=128)
    full_name = models.CharField(max_length=255)
    nick_name = models.CharField(max_length=255, unique=True)
    account_balance = models.DecimalField(max_digits=16, decimal_places=2, default=0.00)
    date_of_birth = models.DateField()
    pesel = models.CharField(max_length=11, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()  # assigns custom user manager to objects attribute

    USERNAME_FIELD = 'email'  # default is username
    REQUIRED_FIELDS = ['full_name', 'nick_name', 'date_of_birth', 'pesel']
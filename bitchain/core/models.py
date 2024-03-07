"""
Models for the core app of the project, mostly for user related data
"""
import os
import uuid

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)

from django_rest_passwordreset.signals import reset_password_token_created
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


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


def get_upload_path(instance, filename):
    ext = os.path.splitext(filename)[1]
    filename = f'{instance.id}{ext}'

    return os.path.join('uploads', 'user',  filename)


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=128)
    full_name = models.CharField(max_length=255)
    nick_name = models.CharField(max_length=255, unique=True)
    account_balance = models.DecimalField(max_digits=16, decimal_places=2, default=0.00)
    date_of_birth = models.DateField()
    pesel = models.CharField(max_length=11)
    image = models.ImageField(null=True, upload_to=get_upload_path, blank=True, default=os.path.join('uploads', 'user',
                                                                                                      'default.jpg'))

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()  # assigns custom user manager to objects attribute

    USERNAME_FIELD = 'email'  # default is username
    REQUIRED_FIELDS = ['full_name', 'nick_name', 'date_of_birth', 'pesel']

    def __str__(self):
        return self.email


    @receiver(reset_password_token_created)
    def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
        """
        Handles password reset tokens
        When a token is created, an e-mail needs to be sent to the user
        :param sender: View Class that sent the signal
        :param instance: View Instance that sent the signal
        :param reset_password_token: Token Model Object
        :param args:
        :param kwargs:
        :return:
        """
        
        reset_password_url = f"{settings.FRONTED_URL}/account/reset-password/{reset_password_token.key}"
        
        # send an e-mail to the user
        context = {
            'username': reset_password_token.user.nick_name,
            'email': reset_password_token.user.email,
            'reset_password_url': reset_password_url,
        }

        # render email text
        email_html_message = render_to_string('core/user_reset_password_email.html', context)
        email_plaintext_message = strip_tags(email_html_message)

        msg = EmailMultiAlternatives(
            # title:
            "BitChain Password Reset - {reset_password_token.user.nick_name}",
            # message:
            email_plaintext_message,
            # from:
            settings.DEFAULT_FROM_EMAIL,
            # to:
            [reset_password_token.user.email]
        )
        msg.attach_alternative(email_html_message, "text/html")
        msg.send()


class FavoriteUserCryptocurrency(models.Model):
    """Model for storing multiple favorite cryptocurrencies for a user"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    favorite_crypto_symbol = models.CharField(max_length=10)

    class Meta:
        unique_together = ('user', 'favorite_crypto_symbol')


    def __str__(self):
        return f'{self.user.email} - {self.favorite_crypto_symbol}'
    


class UserGenericWallet(models.Model):
    
    
    class Meta:
        abstract = True 


class UserFeatureWallet(UserGenericWallet):
    pass
    

class UserStackingWallet(UserGenericWallet):
    pass


class UserFundWallet(UserGenericWallet):
    pass


class UserWalletOverview(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fund_wallet = models.OneToOneField(UserFeatureWallet, on_delete=models.CASCADE)
    stacking_wallet = models.OneToOneField(UserFeatureWallet, on_delete=models.CASCADE)
    feature_wallet = models.OneToOneField(UserFeatureWallet, on_delete=models.CASCADE)
    

class UserWalletCryptocurrency(models.Model):
    wallet = models.ForeignKey(UserGenericWallet, on_delete=models.CASCADE)
    cryptocurrency_symbol = models.CharField(max_length=10)
    cryptocurrency_amount = models.DecimalField(max_digits=16, decimal_places=10, default=0.00)

    def __str__(self):
        return f"{self.wallet.user.username} - {self.cryptocurrency_symbol} - {self.cryptocurrency_amount}"
    
class UserTransaction(models.Model):
    """Model for storing user transactions"""
    user_wallet_type = models.ForeignKey(UserGenericWallet, on_delete=models.CASCADE)
    transcation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    transaction_type = models.CharField(max_length=10)
    transaction_amount = models.IntegerField()
    transcation_currency = models.CharField(max_length=10)
    transaction_price_usd = models.DecimalField(max_digits=16, decimal_places=2)
    transaction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.email}'

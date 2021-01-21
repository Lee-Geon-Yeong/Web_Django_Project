from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _
from allauth.account.models import EmailAddress, EmailAddressManager
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.models import EmailAddressManager, EmailAddress
from allauth.account.utils import user_field
from carts.models import Cart

# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


import datetime


class Account(AbstractUser):
    SEX_CHOICES = [(0, "Female"), (1, "Male")]
    sex = models.BooleanField(verbose_name='sex',
                              null=True,
                              default=None,
                              choices=SEX_CHOICES)
    age = models.PositiveSmallIntegerField(null=True, default=None)
    username = None
    email = models.EmailField(_('email address'), unique=True, blank=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['sex', 'age']
    objects = CustomUserManager()

    def __str__(self):
        return self.email.split('@')[0]


class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form):
        ret = super().save_user(request, user, form)
        cart_obj = Cart.objects.create(total_price=None, user=user)
        cart_obj.save()
        return ret


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        u = super().save_user(request, sociallogin, form)
        cart_obj = Cart.objects.create(total_price=None, user=u)
        cart_obj.save()
        return u


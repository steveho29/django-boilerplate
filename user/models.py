from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
import logging

class SOCIAL_AUTH_PLATFORM(models.TextChoices):
    NONE = 'NONE', _('NONE')
    GOOGLE = 'GOOGLE', _('GOOGLE')

class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        """
            Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_verified', True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser):
    class Meta:
        db_table = 'user'

    objects = UserManager()

    username = None
    USERNAME_FIELD = 'email'
    
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    
    first_name = models.TextField(max_length=20)
    last_name = models.TextField(max_length=50, null=True)
    date_of_birth = models.DateField(null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    avatar = models.ImageField(upload_to='images', null=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    email_verified= models.BooleanField(default=False)
    email_code = models.CharField(max_length=100, null=True)
    social_auth = models.CharField(max_length=20,choices=SOCIAL_AUTH_PLATFORM.choices, default=SOCIAL_AUTH_PLATFORM.NONE)
    
    REQUIRED_FIELDS = ['first_name', 'last_name',
                       'date_of_birth',]


    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
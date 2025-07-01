from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from utils.exceptions import BadRequestException
from django.db import models
from django.utils import timezone
from utils.models import BaseModel

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise BadRequestException()
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser, PermissionsMixin,BaseModel):
    
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('manager', 'HotelManager'),
        ('customer', 'Customer'),
    )
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')


    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

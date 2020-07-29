from porsgram.settings import MEDIA_ROOT

from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
from PIL import Image
from pathlib import Path


import os
# Create your models here.

class UserModel(AbstractBaseUser, PermissionsMixin):
    STATUS_CHOICES = (
        ('female', 'مونث'),
        ('male', 'مذکر'),
        ('none', 'به تو چه'),
    )

    id         = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=20, blank=False)
    last_name  = models.CharField(max_length=20, blank=True)
    password   = models.CharField(max_length=100)
    username   = models.CharField(max_length=30, unique=True, blank=False)
    email      = models.EmailField(unique=True, blank=False)
    join_date  = models.DateField(auto_now_add=True)
    last_seen  = models.DateTimeField(auto_now_add=True)
    reputation = models.PositiveIntegerField(default=0)
    is_staff   = models.BooleanField(default=False)
    gender     = models.CharField(max_length=6, choices=STATUS_CHOICES, default='none')

    # objects       = models.Manager()
    objects    = UserManager()

    USERNAME_FIELD  = 'username'
    REQUIRED_FIELDS = []



class AvatarModel(models.Model):
    user    = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    avatar  = models.ImageField(default='default.png', upload_to='avatar')
    objects = models.Manager()


    # def save(self, is_update):
    def save(self, force_insert=False, force_update=False, using=None):
        super().save()
        SIZE      = 200
        FILE_SCALE = (SIZE, SIZE)

        img = Image.open(self.avatar.path)

        if img.width > SIZE or img.height > SIZE:
            img.thumbnail(FILE_SCALE)
            img.save(self.avatar.path)




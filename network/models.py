from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    profile_pic = models.ImageField(blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)


class Hometown(models.Model):

    hometown = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.hometown}"
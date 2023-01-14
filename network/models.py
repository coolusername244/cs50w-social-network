from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Hometown(models.Model):

    hometown = models.CharField(max_length=100)
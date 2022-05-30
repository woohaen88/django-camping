from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    class Meta:
        verbose_name_plural = "User"  # admin model 변경

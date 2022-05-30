from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "User"  # admin model 변경


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Post(TimeStampedModel):
    title = models.CharField(max_length=15)
    review = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    thumbnail = models.ImageField(upload_to="image/thumbnail/%Y/%m/%d")

    class Meta:
        verbose_name_plural = "Post"

    def __str__(self):
        return f"{self.title}"

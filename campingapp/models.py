from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
from django.urls import reverse_lazy, reverse


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


class Category(models.Model):

    name = models.CharField(max_length=15, unique=True)
    slug = models.SlugField(max_length=30, unique=True, allow_unicode=True)

    def get_absolute_url(self):
        return f"/camping/category/{self.slug}/"

    def __str__(self):
        return self.name

    # class Meta:
    #     verbose_name_plural = "Categories"


class Tag(models.Model):
    name = models.CharField(max_length=10)
    slug = models.SlugField(max_length=40, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"/camping/tag/{self.slug}/"


class Post(TimeStampedModel):
    title = models.CharField(max_length=15)
    review = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    thumbnail = models.ImageField(upload_to="image/thumbnail/%Y/%m/%d")
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    tags = models.ManyToManyField(Tag, blank=True)

    class Meta:
        verbose_name_plural = "Post"

    def __str__(self):
        return f"{self.title}"


class Comment(TimeStampedModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comment")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment")
    content = models.TextField()

    def get_absolute_url(self):
        return reverse("campingapp:new_comment", kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.author}::{self.content}"

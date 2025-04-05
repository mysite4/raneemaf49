from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
import uuid


# نموذج الفئة (Category)
class Category(models.Model):
    name = models.CharField('categories', max_length=50)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


# نموذج الكتاب (Book)
class Book(models.Model):
    title = models.CharField(max_length=100)
    cover_image = models.ImageField(upload_to='img', blank=True, null=True)
    author = models.CharField(max_length=50)
    category = models.ManyToManyField(Category, related_name='books')
    pdf = models.FileField(upload_to='pdf')
    is_recommended = models.BooleanField(default=False)
    is_fiction = models.BooleanField(default=False)
    is_business = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return self.title


# نموذج العضو (Member)
class Member(models.Model):
    name = models.CharField(max_length=100, default="Unnamed")
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.name


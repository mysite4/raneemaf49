from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import uuid



class CustomUser(AbstractUser):
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_groups',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )
    
    

    def __str__(self):
        return self.username


# TeamMember Manager
class TeamMemberManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by('-created_at')

class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    image = models.ImageField(upload_to='team_images/')
    created_at = models.DateTimeField(auto_now_add=True)
     
    
    objects = TeamMemberManager()  # Manager for TeamMember

    def __str__(self):
        return self.name


# Post Manager
class PostManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by('-created')

class Post(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    image = models.URLField(max_length=500, blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="posts")
    rating = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    objects = PostManager()  # Manager for Post

    def __str__(self):
        return self.title


# Tag Manager
class TagManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by('name')

class Tag(models.Model):
    name = models.CharField(max_length=20)
    image = models.FileField(upload_to='icons/', null=True, blank=True)
    slug = models.SlugField(max_length=20, unique=True)
    order = models.IntegerField(null=True)

    objects = TagManager()  # Manager for Tag

    def __str__(self):
        return self.name


# Comment Manager
class CommentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by('-created')

class Comment(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL,
        null=True,
        related_name='comments'
    )
    parent_post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    body = models.CharField(max_length=150)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    objects = CommentManager()  # Manager for Comment

    def __str__(self):
        try:
            return f'{self.author.username} : {self.body[:30]}'
        except AttributeError:
            return f'Unknown Author: {self.body[:30]}'


# NewsItem Manager
class NewsItemManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by('-publish_date')

class NewsItem(models.Model):
    name = models.CharField(max_length=200)
    job_title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='news_images/')
    rating = models.PositiveIntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)
    publish_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    link = models.URLField(max_length=200, null=True, blank=True)

    objects = NewsItemManager()  # Manager for NewsItem

    def __str__(self):
        return self.name


# News Manager
class NewsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by('-rating')

class News(models.Model):
    name = models.CharField(max_length=200)
    job_title = models.CharField(max_length=100)
    rating = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='news_images/')

    objects = NewsManager()  # Manager for News

    def __str__(self):
        return self.name


# Member Manager
class MemberManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by('-id')

class Member(models.Model):
    name = models.CharField(max_length=100, default="Unnamed")
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    objects = MemberManager()  # Manager for Member

    def __str__(self):
        return self.name


# Progress Manager
class ProgressManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by('-id')

class Progress(models.Model):
    partner = models.IntegerField(default=0)
    employee = models.IntegerField(default=0)
    client = models.IntegerField(default=0)
    job = models.IntegerField(default=0)

    objects = ProgressManager()  # Manager for Progress

    def __str__(self):
        return f"Progress {self.id}"


# Message Manager
class MessageManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by('-date')

class Message(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='sent_messages'
    )
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='received_messages'
    )
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    objects = MessageManager()  # Manager for Message


# ContactMessage Manager
class ContactMessageManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by('-date_sent')

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    date_sent = models.DateTimeField(auto_now_add=True)

    objects = ContactMessageManager()  # Manager for ContactMessage

    def __str__(self):
        return f"Message from {self.name} at {self.date_sent}"

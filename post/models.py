import uuid
from django.conf import settings
from django.db import models
from django.utils import timezone
from core import settings
from account.models import *


# class UploadedFile(models.Model):
#     file = models.FileField(upload_to='uploads/')
#     uploaded_at = models.DateTimeField(auto_now_add=True)
#
#     @property
#     def file_url(self):
#         # Assuming MEDIA_URL is '/media/'
#         return f"{settings.MEDIA_URL}{self.file.name}"


class Like(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name='likes', blank=True)

    def __str__(self):
        return self.owner


class Post(models.Model):
    DATA_TYPE_CHOICES = [
        ('text', 'Text'),
        ('image', 'Image'),
        ('video', 'Video'),
        ('other', 'Other'),
    ]

    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_posts')
    title = models.CharField(max_length=250)
    body = models.TextField()
    data_type = models.CharField(max_length=10, choices=DATA_TYPE_CHOICES)
    data = models.FileField(upload_to='posts/data/', blank=True, null=True)
    upload_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user} on {self.post}'
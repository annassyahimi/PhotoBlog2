from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User 

class Post(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    text = models.TextField(blank=True, null=True)                
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    author = models.CharField(max_length=100, blank=True, null=True)  
    created_at = models.DateTimeField(auto_now_add=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title or "Untitled"
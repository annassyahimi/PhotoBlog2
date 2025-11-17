from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User 

class Post(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField(blank=True, null=True) 
    image = models.ImageField(upload_to='intruder_image/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return f"{self.title} - {self.created_at}"
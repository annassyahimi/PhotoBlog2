from blog.models import Post
from rest_framework import serializers
from django.contrib.auth.models import User

class PostSerializers(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__' 

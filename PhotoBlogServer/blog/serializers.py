from blog.models import Post
from rest_framework import serializers
from django.contrib.auth.models import User

class PostSerializers(serializers.ModelSerializer):

    content = serializers.CharField(source='text', required=False)
    created_date = serializers.DateTimeField(source='created_at', read_only=True)
    
    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'created_date',
            'image',
        ]
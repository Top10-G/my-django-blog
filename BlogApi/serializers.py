from rest_framework import serializers
from post.models import Post

class PostSerializer(serializers.ModelSerializer): #
  
    owner = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'owner', 'created_at', 'updated_at']
        
        
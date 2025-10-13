from django.shortcuts import render
from rest_framework import viewsets

from BlogApi.serializers import PostSerializer
from post.models import Post

# Create your views here.


class PostViewSet(viewsets.ModelViewSet):
  queryset = Post.objects.all()
  serializer_class = PostSerializer
  

  def perform_create(self, serializer):
    serializer.save(owner=self.request.user)
    
    
    

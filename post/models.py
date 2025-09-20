from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):

  owner = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)

  title = models.CharField(max_length=50)
  
  content = models.TextField()
  
  image = models.ImageField(upload_to='images/', null=True, blank=True)
  
  created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True) #this is for when you create a post
  
  updated_at = models.DateTimeField(auto_now=True, null=True, blank=True) #this is for when you update a post

  def __str__(self):
    return f"Title: {self.title}, Content: {self.content}"


# Routes
# GET, PUT, PATCH, POST, DELETE

# GET /posts => Get all posts
# POST /posts => Create a post
# GET /posts/:id => Get a post by id
# DELETE /posts/:id => Delete a post by id
# PUT /posts/:id => update a post by id

# GET /books => Get all books
# GET /books/:id =>
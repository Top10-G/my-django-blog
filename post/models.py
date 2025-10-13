from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from PIL import Image
# Create your models here.

class Post(models.Model):

  owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='posts', on_delete=models.CASCADE)

  title = models.CharField(max_length=50)
  
  content = models.TextField()
  
  image = models.ImageField(upload_to='images/', null=True, blank=True)
  
  created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True) #this is for when you create a post
  
  updated_at = models.DateTimeField(auto_now=True, null=True, blank=True) #this is for when you update a post

  likes = models.ManyToManyField(User, related_name='liked_posts', blank=True) # this is for the like feature... many users can like many posts... hence many to many relationship
  
  def __str__(self):
    return f"Title: {self.title}, Content: {self.content}"


# ===========================================================================


# ==============================
# PROFILE MODEL
# ==============================
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=150, blank=True)
    image = models.ImageField(upload_to='profile_pics/', default='profile_pics/default.png')
    bio = models.TextField(blank=True, default='')

    def __str__(self):
        return self.display_name or self.user.username





class Comment(models.Model):
    post = models.ForeignKey(
        'Post',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replies'
    )

    class Meta:
        ordering = ['created_at']  # oldest first (good for comments)

    def __str__(self):
        return f'Comment by {self.user} on {self.post}'





# Routes
# GET, PUT, PATCH, POST, DELETE

# GET /posts => Get all posts
# POST /posts => Create a post
# GET /posts/:id => Get a post by id
# DELETE /posts/:id => Delete a post by id
# PUT /posts/:id => update a post by id

# GET /books => Get all books
# GET /books/:id =>
from django.urls import path
from .views import post_list, single_post, new_post, edit_post,delete_post


urlpatterns = [
  path('posts/', post_list, name='post_list'),

  path('posts/new', new_post, name='create_post'),

  path('posts/<int:post_id>', single_post, name='single_post'),
  
  
  path('posts/<int:post_id>/edit', edit_post, name='edit_post'),

  path('posts/<int:post_id>/delete', delete_post, name='delete_post'),

]


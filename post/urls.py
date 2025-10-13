from django.urls import path, include

from post import views as post_views
from .views import CustomPasswordChangeView, like_post, post_list, single_post, new_post, edit_post,delete_post, search_posts, add_comment, delete_comment, profile_view, edit_profile, about


urlpatterns = [
  
  path('posts/', post_list, name='post_list'),

  path('posts/new', new_post, name='create_post'),

  path('posts/<int:post_id>', single_post, name='single_post'),
  
  
  path('posts/<int:post_id>/edit', edit_post, name='edit_post'),

  path('posts/<int:post_id>/delete', delete_post, name='delete_post'),

  path('search/', search_posts, name='search'),
  
  path('posts/<int:post_id>/like', like_post, name='like_post'),  
  
  path('posts/<int:post_id>/comment/', add_comment, name='add_comment'),
  
  path('comments/<int:comment_id>/delete/', delete_comment, name='delete_comment'),
  
  path('profile/edit/', edit_profile, name='edit_profile'),

  path('profile/change-password/', CustomPasswordChangeView.as_view(), name='change_password'),
  
  path('profile/<str:username>/', profile_view, name='profile'),
  
]


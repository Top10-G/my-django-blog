
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required 
from django.db.models import Q
from.models import Post, Comment, Profile
from django.contrib import messages
from .forms import CommentForm, PostForm, UserUpdateForm, ProfileForm
from django.urls import reverse
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User


@login_required
def post_list(request): #this is to fetch all post
  posts = Post.objects.all
  # posts = Post.objects.filter(owner=request.user) #this is to fetch all posts from the database that belong to the currently logged in user
  temp_var = {"allposts": posts} 
  return render(request, "post_list.html", temp_var) #note that the post_list here is not the function name... it is the name of the template that the posts are being sent to. when you check the templates folder, you will see an html file called post_list.html

@login_required
def new_post(request):
  form = None # initialize form variable
  if (request.method == "POST"):
    form = PostForm(request.POST, request.FILES) #request.FILES is for the image field
    if (form.is_valid()):
      post = form.save(commit=False) #commit=False is to prevent the form from being saved to the database immediately... don't save it yet, i want to add a user 
      post.owner = request.user # this is to set the owner of the post to the currently logged in user
      post.save()
      return redirect("post_list")

  else:
    form = PostForm() #create an empty form
    
  print(form['title'].value()) # to print the title value in the console if there is any
  print(form.errors) # to print the form errors in the console if there are any
  return render(request, "new_post.html", {'form': form}) # we added 'form': form to be able to access the form in the template

@login_required
def edit_post(request, post_id):
  post = get_object_or_404(Post, id=post_id)
  if request.user != post.owner:
      return HttpResponse("Unauthorized", status=401)

  if request.method == 'POST':
      form = PostForm(request.POST, request.FILES, instance=post)
      if form.is_valid():
          form.save()
          return redirect('single_post', post_id=post.id)
  else:
      form = PostForm(instance=post)
  
  return render(request, 'edit_post.html', {'form': form, 'post': post})


@login_required
def delete_post(request, post_id):
  post = get_object_or_404(Post, id=post_id)

  if post.owner != request.user:
    messages.error(request, "You are not allowed to delete this post.")
    return redirect('single_post', post_id=post.id)

  if request.method == 'POST':
    post.delete()
    messages.success(request, "Post deleted successfully.")
    return redirect('post_list')

  return render(request, 'post/confirm_delete_post.html', {'post': post})


@login_required
def single_post(request, post_id):
  post = get_object_or_404(Post, id=post_id)
  form = CommentForm()  # Initialize an empty comment form
  return render(request, 'single_post.html', {'singlepost': post, 'form': form})



def search_posts(request):
  query = request.GET.get('q', '')
  results = []
  
  if query:
      results = Post.objects.filter(
          Q(title__icontains=query) | Q(content__icontains=query)
      ).order_by('-created_at')

  return render(request, 'search_results.html', {
      'allposts': results,
      'query': query
  })


@login_required
def like_post(request, post_id):
  post = get_object_or_404(Post, id=post_id)

  if request.user in post.likes.all():
    post.likes.remove(request.user)
  else:
    post.likes.add(request.user)

  return redirect('post_list')


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            messages.success(request, "Comment posted.")
        else:
            messages.error(request, "Comment cannot be empty.")
    # redirect back to the post detail page
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    return redirect('single_post', post_id=post.id)


@login_required
def delete_comment(request, comment_id):
  comment = get_object_or_404(Comment, id=comment_id)

    # 🛡️ Ownership check (comment owner or post owner)
  if request.user != comment.user and request.user != comment.post.owner:
    messages.error(request, "You are not allowed to delete this comment.")
    return redirect('single_post', post_id=comment.post.id)

  if request.method == 'POST':
    comment.delete()
    messages.success(request, "Comment deleted.")
    return redirect('single_post', post_id=comment.post.id)

  return render(request, 'post/confirm_delete.html', {'comment': comment})




#==========================================================================


@login_required
def profile_view(request, username):
    """
    Show a user's profile by username.
    """
    user = get_object_or_404(User, username=username)
    profile = getattr(user, 'profile', None)
    return render(request, 'profile.html', {'profile': profile, 'profile_user': user})



@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile', username=request.user.username)  # FIXED
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }

    return render(request, 'edit_profile.html', context)
  


# ==========================================================================


class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'change_password.html'

    def get_success_url(self):
        """Redirect to the user's profile after successful password change."""
        return reverse('profile', kwargs={'username': self.request.user.username})

    def form_valid(self, form):
        messages.success(self.request, "Your password was changed successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)



# ===========================================================================


def home(request):
    if request.user.is_authenticated:
        return redirect('post_list')  # take logged-in users to posts
    return render(request, 'home.html')
  
# ===========================================================================


def about(request):
    return render(request, 'about.html')


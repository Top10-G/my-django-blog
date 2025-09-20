from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required 

from.models import Post
from .forms import PostForm

# Create your views here.

@login_required
def post_list(request): #this is to fetch all post
  posts = Post.objects.filter(owner=request.user) #this is to fetch all posts from the database that belong to the currently logged in user
  # posts = Post.objects.all() #this is to fetch all posts from the database
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
  post = Post.objects.get(id=post_id)

  if (request.method == "POST"):
    form = PostForm(request.POST, request.FILES, instance=post)
    if (form.is_valid()):
      form.save()
      return redirect("post_list")

  else:
    form = PostForm(instance=post) #create an empty form

  return render(request, "edit_post.html", {'post': post})



@login_required
def delete_post(request, post_id):
  post = Post.objects.get(id=post_id)
  
  if (request.method == "POST"):
    post.delete()
    
  return redirect('post_list')


@login_required
def single_post(request, post_id):
  post = get_object_or_404(Post, id=post_id)
  return render(request, 'single_post.html', {'singlepost': post})


# def single_post(request, post_id): #this is to fetch a single post
#   post = Post.objects.get(id=post_id)
#   return render(request, "single_post.html", {"post": post, "id": post_id})


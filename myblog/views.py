from django.shortcuts import redirect, render
from post.forms import SignUpForm
# from django.contrib.auth import login


def signup(request):
  form = None
  if (request.method == "POST"): # if the request method is POST
    form = SignUpForm(request.POST) 
    print('signup test')
    print(form.errors)
    if (form.is_valid()):
      print('checking for redirect 111')
      form.save()
      # user = form.save()
      # login(request, user) This line is to log the user in automatically after signup
      return redirect('login') # we redirect to the login page after successful signup
  else:
    form = SignUpForm()
  return render(request, 'signup.html', {'signupform': form}) # we added 'signupform': form to be able to access the form in the template
from django.contrib import messages
from django.shortcuts import render, redirect
from post.forms import SignUpForm

def signup(request):
    # Clear any old messages on page load (GET request)
    if request.method == 'GET':
        storage = messages.get_messages(request)
        storage.used = True  # Mark all messages as read/used
        form = SignUpForm()
    
    # Handle form submission (POST request)
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! You can now log in.")
            return redirect('login')
        else:
            messages.error(request, "Please correct the errors below.")

    return render(request, 'signup.html', {'signupform': form})







# from django.shortcuts import render, redirect
# from django.contrib import messages
# from post.forms import SignUpForm

# def signup(request):
#     if request.method == "POST":
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Account created successfully! You can now log in.")
#             return redirect('login')
#         else:
#             messages.error(request, "Please correct the errors below.")
#     else:
#         form = SignUpForm()

#     return render(request, 'signup.html', {'signupform': form})

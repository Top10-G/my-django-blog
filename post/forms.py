from xml.etree.ElementTree import Comment
from django import forms
from.models import Post, Comment, Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 

bad_words = ['bad', 'ugly', 'nasty', 'stupid', 'dumb', 'foolish', 'idiot', 'fool', 'moron', 'loser']

class PostForm(forms.ModelForm):
    
    title = forms.CharField(required=False) #this is to override the default behavior of the title field in the model to make it required

    content = forms.CharField(required=False) #this is to override the default behavior of the content field in the model to make it required

    
    
    class Meta:
        model = Post
        fields = ['title', 'content', 'image']
        
        
    
    def clean_title(self):
    
        title = self.cleaned_data.get('title')
        if (title == ''):
            raise forms.ValidationError('Title cannot be empty')
        return title

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if (content == ''):
            raise forms.ValidationError('Content cannot be empty')

        found_bad_words = []
        
        for word in bad_words:
            if word in content:
                found_bad_words.append(word)
            
        if len(found_bad_words) > 0:
            raise forms.ValidationError(f'The content cannot contain inappropriate words: {',' .join(found_bad_words)}')
        return content
    
class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=False)
    username = forms.CharField(required=False)
    

    class Meta:
        model = User 
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name']
    
    def clean_email(self):
        print('hello')
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already exists')
        print('email test')
        return email
    
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if (first_name == ''):
            raise forms.ValidationError('First name cannot be empty')
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if (last_name == ''):
            raise forms.ValidationError('Last name cannot be empty')
        return last_name
    

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'parent']   # include parent if you want replies
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Write a comment...',
                'class': 'comment-textarea'
            }),
            'parent': forms.HiddenInput(),  # parent set via template if threading
        }


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']  # 👈 include username here
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email'
            }),
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['display_name', 'bio', 'image']
        widgets = {
            'display_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter display name'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write a short bio',
                'rows': 4
            }),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

